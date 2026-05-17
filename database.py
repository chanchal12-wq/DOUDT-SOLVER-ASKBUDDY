import sqlite3
from flask import g
from werkzeug.security import generate_password_hash
import os

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'askbuddy.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database with tables and admin user"""
    try:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        db = sqlite3.connect(DATABASE)
        
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                reputation_points INTEGER DEFAULT 0,
                profile_photo TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add profile_photo column if it doesn't exist (for existing databases)
        try:
            db.execute('ALTER TABLE users ADD COLUMN profile_photo TEXT DEFAULT NULL')
        except Exception:
            pass
        
        db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                subject TEXT NOT NULL,
                tags TEXT,
                image TEXT,
                status TEXT DEFAULT 'unsolved',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        db.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                answer_text TEXT NOT NULL,
                votes INTEGER DEFAULT 0,
                is_best_answer INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        db.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                answer_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                vote_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (answer_id) REFERENCES answers (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(answer_id, user_id)
            )
        ''')
        
        db.execute('''
            CREATE TABLE IF NOT EXISTS study_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                file TEXT NOT NULL,
                subject TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES users (id)
            )
        ''')
        
        # Create admin account if not exists
        admin = db.execute('SELECT id FROM users WHERE email = ?', ('admin@askbuddy.com',)).fetchone()
        if not admin:
            hashed_password = generate_password_hash('admin123')
            db.execute('INSERT INTO users (name, email, password, role, reputation_points) VALUES (?, ?, ?, ?, ?)',
                       ('Admin', 'admin@askbuddy.com', hashed_password, 'admin', 0))
        
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
