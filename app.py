from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime
from models.database import init_db, get_db
import sqlite3

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize database when app starts
with app.app_context():
    init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Role required decorator
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('Access denied', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    db = get_db()
    stats = {
        'total_users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
        'total_questions': db.execute('SELECT COUNT(*) FROM questions').fetchone()[0],
        'total_answers': db.execute('SELECT COUNT(*) FROM answers').fetchone()[0],
        'solved_questions': db.execute('SELECT COUNT(*) FROM questions WHERE status = "solved"').fetchone()[0]
    }
    
    recent_questions = db.execute('''
        SELECT q.*, u.name as author_name, 
        (SELECT COUNT(*) FROM answers WHERE question_id = q.id) as answer_count
        FROM questions q
        JOIN users u ON q.user_id = u.id
        ORDER BY q.created_at DESC LIMIT 6
    ''').fetchall()
    
    return render_template('index.html', stats=stats, recent_questions=recent_questions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        db = get_db()
        
        if db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        db.execute('INSERT INTO users (name, email, password, role, reputation_points) VALUES (?, ?, ?, ?, ?)',
                   (name, email, hashed_password, role, 0))
        db.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            session['reputation'] = user['reputation_points']
            session['profile_photo'] = user['profile_photo']
            
            flash(f'Welcome back, {user["name"]}!', 'success')
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# Student Dashboard
@app.route('/student/dashboard')
@login_required
@role_required(['student'])
def student_dashboard():
    db = get_db()
    
    my_questions = db.execute('''
        SELECT q.*, (SELECT COUNT(*) FROM answers WHERE question_id = q.id) as answer_count
        FROM questions q WHERE q.user_id = ? ORDER BY q.created_at DESC LIMIT 5
    ''', (session['user_id'],)).fetchall()
    
    my_answers = db.execute('''
        SELECT a.*, q.title as question_title
        FROM answers a
        JOIN questions q ON a.question_id = q.id
        WHERE a.user_id = ? ORDER BY a.created_at DESC LIMIT 5
    ''', (session['user_id'],)).fetchall()
    
    stats = {
        'questions_posted': db.execute('SELECT COUNT(*) FROM questions WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'answers_given': db.execute('SELECT COUNT(*) FROM answers WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'reputation': session['reputation'],
        'best_answers': db.execute('SELECT COUNT(*) FROM answers WHERE user_id = ? AND is_best_answer = 1', (session['user_id'],)).fetchone()[0]
    }
    
    return render_template('student_dashboard.html', my_questions=my_questions, my_answers=my_answers, stats=stats)

# Post Question
@app.route('/student/ask', methods=['GET', 'POST'])
@login_required
@role_required(['student'])
def ask_question():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        subject = request.form['subject']
        tags = request.form['tags']
        
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'questions', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                image = f'uploads/questions/{filename}'
        
        db = get_db()
        db.execute('''
            INSERT INTO questions (user_id, title, description, subject, tags, image, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], title, description, subject, tags, image, 'unsolved'))
        db.commit()
        
        flash('Question posted successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    
    # Get similar questions for suggestion
    similar_questions = []
    if request.args.get('title'):
        title = request.args.get('title')
        db = get_db()
        similar_questions = db.execute('''
            SELECT * FROM questions WHERE title LIKE ? LIMIT 5
        ''', (f'%{title}%',)).fetchall()
    
    return render_template('ask_question.html', similar_questions=similar_questions)

# View All Questions
@app.route('/questions')
@login_required
def view_questions():
    db = get_db()
    
    subject = request.args.get('subject', '')
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = '''
        SELECT q.*, u.name as author_name,
        (SELECT COUNT(*) FROM answers WHERE question_id = q.id) as answer_count
        FROM questions q
        JOIN users u ON q.user_id = u.id
        WHERE 1=1
    '''
    params = []
    
    if subject:
        query += ' AND q.subject = ?'
        params.append(subject)
    
    if status:
        query += ' AND q.status = ?'
        params.append(status)
    
    if search:
        query += ' AND (q.title LIKE ? OR q.description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += ' ORDER BY q.created_at DESC'
    
    questions = db.execute(query, params).fetchall()
    subjects = db.execute('SELECT DISTINCT subject FROM questions').fetchall()
    
    return render_template('questions.html', questions=questions, subjects=subjects)

# Question Detail
@app.route('/question/<int:question_id>')
@login_required
def question_detail(question_id):
    db = get_db()
    
    question = db.execute('''
        SELECT q.*, u.name as author_name, u.id as author_id
        FROM questions q
        JOIN users u ON q.user_id = u.id
        WHERE q.id = ?
    ''', (question_id,)).fetchone()
    
    if not question:
        flash('Question not found', 'danger')
        return redirect(url_for('view_questions'))
    
    answers = db.execute('''
        SELECT a.*, u.name as author_name, u.role as author_role
        FROM answers a
        JOIN users u ON a.user_id = u.id
        WHERE a.question_id = ?
        ORDER BY a.is_best_answer DESC, a.votes DESC, a.created_at ASC
    ''', (question_id,)).fetchall()
    
    return render_template('question_detail.html', question=question, answers=answers)

# Submit Answer
@app.route('/question/<int:question_id>/answer', methods=['POST'])
@login_required
def submit_answer(question_id):
    answer_text = request.form['answer_text']
    
    db = get_db()
    db.execute('''
        INSERT INTO answers (question_id, user_id, answer_text, votes, is_best_answer)
        VALUES (?, ?, ?, 0, 0)
    ''', (question_id, session['user_id'], answer_text))
    db.commit()
    
    # Award reputation points
    db.execute('UPDATE users SET reputation_points = reputation_points + 5 WHERE id = ?', (session['user_id'],))
    db.commit()
    session['reputation'] = session['reputation'] + 5
    
    flash('Answer submitted successfully! +5 reputation points', 'success')
    return redirect(url_for('question_detail', question_id=question_id))

# Vote Answer
@app.route('/answer/<int:answer_id>/vote', methods=['POST'])
@login_required
def vote_answer(answer_id):
    vote_type = request.form['vote_type']
    
    db = get_db()
    
    # Check if already voted
    existing_vote = db.execute('SELECT * FROM votes WHERE answer_id = ? AND user_id = ?',
                               (answer_id, session['user_id'])).fetchone()
    
    if existing_vote:
        if existing_vote['vote_type'] == vote_type:
            # Remove vote
            db.execute('DELETE FROM votes WHERE id = ?', (existing_vote['id'],))
            vote_change = -1 if vote_type == 'upvote' else 1
            rep_change = -2 if vote_type == 'upvote' else 2
        else:
            # Change vote
            db.execute('UPDATE votes SET vote_type = ? WHERE id = ?', (vote_type, existing_vote['id']))
            vote_change = 2 if vote_type == 'upvote' else -2
            rep_change = 4 if vote_type == 'upvote' else -4
    else:
        # New vote
        db.execute('INSERT INTO votes (answer_id, user_id, vote_type) VALUES (?, ?, ?)',
                   (answer_id, session['user_id'], vote_type))
        vote_change = 1 if vote_type == 'upvote' else -1
        rep_change = 2 if vote_type == 'upvote' else -2
    
    # Update answer votes
    db.execute('UPDATE answers SET votes = votes + ? WHERE id = ?', (vote_change, answer_id))
    
    # Update author reputation
    answer = db.execute('SELECT user_id FROM answers WHERE id = ?', (answer_id,)).fetchone()
    db.execute('UPDATE users SET reputation_points = reputation_points + ? WHERE id = ?',
               (rep_change, answer['user_id']))
    
    db.commit()
    
    return jsonify({'success': True})

# Mark Best Answer
@app.route('/answer/<int:answer_id>/mark-best', methods=['POST'])
@login_required
def mark_best_answer(answer_id):
    db = get_db()
    
    answer = db.execute('SELECT * FROM answers WHERE id = ?', (answer_id,)).fetchone()
    question = db.execute('SELECT * FROM questions WHERE id = ?', (answer['question_id'],)).fetchone()
    
    # Check if user is question author or teacher
    if question['user_id'] != session['user_id'] and session['role'] != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Remove previous best answer
    db.execute('UPDATE answers SET is_best_answer = 0 WHERE question_id = ?', (answer['question_id'],))
    
    # Mark new best answer
    db.execute('UPDATE answers SET is_best_answer = 1 WHERE id = ?', (answer_id,))
    
    # Update question status
    db.execute('UPDATE questions SET status = "solved" WHERE id = ?', (answer['question_id'],))
    
    # Award reputation to answer author
    db.execute('UPDATE users SET reputation_points = reputation_points + 15 WHERE id = ?', (answer['user_id'],))
    
    db.commit()
    
    flash('Best answer marked! +15 reputation to the author', 'success')
    return jsonify({'success': True})

# Leaderboard
@app.route('/leaderboard')
@login_required
def leaderboard():
    db = get_db()
    
    top_students = db.execute('''
        SELECT u.*, 
        (SELECT COUNT(*) FROM questions WHERE user_id = u.id) as questions_count,
        (SELECT COUNT(*) FROM answers WHERE user_id = u.id) as answers_count,
        (SELECT COUNT(*) FROM answers WHERE user_id = u.id AND is_best_answer = 1) as best_answers_count
        FROM users u
        WHERE u.role = 'student'
        ORDER BY u.reputation_points DESC
        LIMIT 20
    ''').fetchall()
    
    return render_template('leaderboard.html', top_students=top_students)

# Profile
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    db = get_db()
    
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('index'))
    
    questions = db.execute('''
        SELECT q.*, (SELECT COUNT(*) FROM answers WHERE question_id = q.id) as answer_count
        FROM questions q WHERE q.user_id = ? ORDER BY q.created_at DESC
    ''', (user_id,)).fetchall()
    
    answers = db.execute('''
        SELECT a.*, q.title as question_title, q.id as question_id
        FROM answers a
        JOIN questions q ON a.question_id = q.id
        WHERE a.user_id = ? ORDER BY a.created_at DESC
    ''', (user_id,)).fetchall()
    
    stats = {
        'questions_posted': len(questions),
        'answers_given': len(answers),
        'reputation': user['reputation_points'],
        'best_answers': db.execute('SELECT COUNT(*) FROM answers WHERE user_id = ? AND is_best_answer = 1', (user_id,)).fetchone()[0]
    }
    
    return render_template('profile.html', user=user, questions=questions, answers=answers, stats=stats)


# Teacher Dashboard
@app.route('/teacher/dashboard')
@login_required
@role_required(['teacher'])
def teacher_dashboard():
    db = get_db()
    
    recent_questions = db.execute('''
        SELECT q.*, u.name as author_name,
        (SELECT COUNT(*) FROM answers WHERE question_id = q.id) as answer_count
        FROM questions q
        JOIN users u ON q.user_id = u.id
        ORDER BY q.created_at DESC LIMIT 10
    ''').fetchall()
    
    my_answers = db.execute('''
        SELECT a.*, q.title as question_title
        FROM answers a
        JOIN questions q ON a.question_id = q.id
        WHERE a.user_id = ? ORDER BY a.created_at DESC LIMIT 5
    ''', (session['user_id'],)).fetchall()
    
    stats = {
        'total_questions': db.execute('SELECT COUNT(*) FROM questions').fetchone()[0],
        'unsolved_questions': db.execute('SELECT COUNT(*) FROM questions WHERE status = "unsolved"').fetchone()[0],
        'my_answers': db.execute('SELECT COUNT(*) FROM answers WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'active_students': db.execute('SELECT COUNT(DISTINCT user_id) FROM questions').fetchone()[0]
    }
    
    subject_stats = db.execute('''
        SELECT subject, COUNT(*) as count
        FROM questions
        GROUP BY subject
        ORDER BY count DESC
    ''').fetchall()
    
    return render_template('teacher_dashboard.html', recent_questions=recent_questions, 
                         my_answers=my_answers, stats=stats, subject_stats=subject_stats)

# Upload Study Material
@app.route('/teacher/upload-material', methods=['GET', 'POST'])
@login_required
@role_required(['teacher'])
def upload_material():
    if request.method == 'POST':
        title = request.form['title']
        subject = request.form['subject']
        
        if 'file' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'materials', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            db = get_db()
            db.execute('''
                INSERT INTO study_materials (teacher_id, title, file, subject)
                VALUES (?, ?, ?, ?)
            ''', (session['user_id'], title, f'uploads/materials/{filename}', subject))
            db.commit()
            
            flash('Study material uploaded successfully!', 'success')
            return redirect(url_for('teacher_dashboard'))
    
    return render_template('upload_material.html')

# Study Materials
@app.route('/materials')
@login_required
def study_materials():
    db = get_db()
    
    subject = request.args.get('subject', '')
    
    query = '''
        SELECT sm.*, u.name as teacher_name
        FROM study_materials sm
        JOIN users u ON sm.teacher_id = u.id
        WHERE 1=1
    '''
    params = []
    
    if subject:
        query += ' AND sm.subject = ?'
        params.append(subject)
    
    query += ' ORDER BY sm.created_at DESC'
    
    materials = db.execute(query, params).fetchall()
    subjects = db.execute('SELECT DISTINCT subject FROM study_materials').fetchall()
    
    return render_template('study_materials.html', materials=materials, subjects=subjects)

# Delete Answer (Teacher/Admin)
@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
@login_required
@role_required(['teacher', 'admin'])
def delete_answer(answer_id):
    db = get_db()
    
    answer = db.execute('SELECT * FROM answers WHERE id = ?', (answer_id,)).fetchone()
    if answer:
        question_id = answer['question_id']
        db.execute('DELETE FROM votes WHERE answer_id = ?', (answer_id,))
        db.execute('DELETE FROM answers WHERE id = ?', (answer_id,))
        db.commit()
        flash('Answer deleted successfully', 'success')
        return redirect(url_for('question_detail', question_id=question_id))
    
    flash('Answer not found', 'danger')
    return redirect(url_for('view_questions'))

# Admin Dashboard
@app.route('/admin/dashboard')
@login_required
@role_required(['admin'])
def admin_dashboard():
    db = get_db()
    
    stats = {
        'total_users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
        'total_students': db.execute('SELECT COUNT(*) FROM users WHERE role = "student"').fetchone()[0],
        'total_teachers': db.execute('SELECT COUNT(*) FROM users WHERE role = "teacher"').fetchone()[0],
        'total_questions': db.execute('SELECT COUNT(*) FROM questions').fetchone()[0],
        'total_answers': db.execute('SELECT COUNT(*) FROM answers').fetchone()[0],
        'solved_questions': db.execute('SELECT COUNT(*) FROM questions WHERE status = "solved"').fetchone()[0]
    }
    
    recent_users = db.execute('''
        SELECT * FROM users ORDER BY created_at DESC LIMIT 10
    ''').fetchall()
    
    subject_stats = db.execute('''
        SELECT subject, COUNT(*) as count
        FROM questions
        GROUP BY subject
        ORDER BY count DESC
    ''').fetchall()
    
    top_students = db.execute('''
        SELECT * FROM users WHERE role = "student"
        ORDER BY reputation_points DESC LIMIT 5
    ''').fetchall()
    
    return render_template('admin_dashboard.html', stats=stats, recent_users=recent_users,
                         subject_stats=subject_stats, top_students=top_students)

# User Management
@app.route('/admin/users')
@login_required
@role_required(['admin'])
def manage_users():
    db = get_db()
    
    role_filter = request.args.get('role', '')
    
    query = 'SELECT * FROM users WHERE 1=1'
    params = []
    
    if role_filter:
        query += ' AND role = ?'
        params.append(role_filter)
    
    query += ' ORDER BY created_at DESC'
    
    users = db.execute(query, params).fetchall()
    
    return render_template('manage_users.html', users=users)

# Delete User
@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_user(user_id):
    if user_id == session['user_id']:
        flash('Cannot delete your own account', 'danger')
        return redirect(url_for('manage_users'))
    
    db = get_db()
    
    # Delete user's votes
    db.execute('DELETE FROM votes WHERE user_id = ?', (user_id,))
    
    # Delete user's answers
    db.execute('DELETE FROM answers WHERE user_id = ?', (user_id,))
    
    # Delete user's questions
    db.execute('DELETE FROM questions WHERE user_id = ?', (user_id,))
    
    # Delete user
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    db.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('manage_users'))

# Change User Role
@app.route('/admin/user/<int:user_id>/change-role', methods=['POST'])
@login_required
@role_required(['admin'])
def change_user_role(user_id):
    new_role = request.form['role']
    
    db = get_db()
    db.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
    db.commit()
    
    flash('User role updated successfully', 'success')
    return redirect(url_for('manage_users'))

# Delete Question (Admin)
@app.route('/admin/question/<int:question_id>/delete', methods=['POST'])
@login_required
@role_required(['admin', 'teacher'])
def delete_question(question_id):
    db = get_db()
    
    # Delete votes for answers
    db.execute('''
        DELETE FROM votes WHERE answer_id IN 
        (SELECT id FROM answers WHERE question_id = ?)
    ''', (question_id,))
    
    # Delete answers
    db.execute('DELETE FROM answers WHERE question_id = ?', (question_id,))
    
    # Delete question
    db.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    
    db.commit()
    
    flash('Question deleted successfully', 'success')
    return redirect(url_for('view_questions'))

# API for similar questions
@app.route('/api/similar-questions')
@login_required
def api_similar_questions():
    title = request.args.get('title', '')
    
    if len(title) < 3:
        return jsonify([])
    
    db = get_db()
    similar = db.execute('''
        SELECT id, title, subject, status FROM questions 
        WHERE title LIKE ? 
        ORDER BY created_at DESC LIMIT 5
    ''', (f'%{title}%',)).fetchall()
    
    return jsonify([dict(q) for q in similar])

# API for analytics data
@app.route('/api/analytics')
@login_required
@role_required(['admin'])
def api_analytics():
    db = get_db()
    
    subject_data = db.execute('''
        SELECT subject, COUNT(*) as count
        FROM questions
        GROUP BY subject
    ''').fetchall()
    
    monthly_data = db.execute('''
        SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count
        FROM questions
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    ''').fetchall()
    
    return jsonify({
        'subjects': [{'subject': row['subject'], 'count': row['count']} for row in subject_data],
        'monthly': [{'month': row['month'], 'count': row['count']} for row in monthly_data]
    })

# Upload Profile Photo
@app.route('/profile/upload-photo', methods=['POST'])
@login_required
def upload_profile_photo():
    if 'photo' not in request.files:
        flash('No file selected', 'danger')
        return redirect(request.referrer or url_for('index'))

    file = request.files['photo']
    if not file or not file.filename:
        flash('No file selected', 'danger')
        return redirect(request.referrer or url_for('index'))

    allowed = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in allowed:
        flash('Invalid file type. Use PNG, JPG, GIF or WEBP.', 'danger')
        return redirect(request.referrer or url_for('index'))

    filename = f"profile_{session['user_id']}.{ext}"
    folder = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles')
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, filename))

    photo_path = f"uploads/profiles/{filename}"
    db = get_db()
    db.execute('UPDATE users SET profile_photo = ? WHERE id = ?', (photo_path, session['user_id']))
    db.commit()
    session['profile_photo'] = photo_path

    flash('Profile photo updated!', 'success')
    return redirect(request.referrer or url_for('index'))


@app.teardown_appcontext
def teardown_db(exception):
    from models.database import close_db
    close_db(exception)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
