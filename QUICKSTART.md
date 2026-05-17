# AskBuddy - Quick Start Guide

## Installation & Setup (3 Easy Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

The script will:
- Initialize the database automatically
- Ask if you want sample data (recommended for testing)
- Start the Flask server

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## Default Login Credentials

### Admin Account
- **Email:** admin@askbuddy.com
- **Password:** admin123

### Sample Student Accounts (if you added sample data)
- **Email:** john@student.com | **Password:** password123
- **Email:** emma@student.com | **Password:** password123

### Sample Teacher Accounts (if you added sample data)
- **Email:** robert@teacher.com | **Password:** password123
- **Email:** lisa@teacher.com | **Password:** password123

## Quick Feature Tour

### As a Student:
1. **Register** → Create account with student role
2. **Ask Question** → Click "Ask New Question" button
3. **Browse Questions** → View and search all questions
4. **Answer Questions** → Help others and earn reputation
5. **Vote** → Upvote helpful answers
6. **Leaderboard** → Check your ranking

### As a Teacher:
1. **Login** → Use teacher account
2. **View Questions** → See all student doubts
3. **Answer** → Provide expert answers
4. **Upload Materials** → Share study resources
5. **Moderate** → Delete inappropriate content
6. **Analytics** → View subject-wise statistics

### As an Admin:
1. **Login** → Use admin credentials
2. **Dashboard** → View system statistics with charts
3. **Manage Users** → Add, delete, or change user roles
4. **Moderate Content** → Remove spam questions/answers
5. **Analytics** → Monitor platform activity

## Key Features to Try

✅ **Similar Question Detection** - Start typing a question title to see suggestions

✅ **Reputation System** - Earn points by answering questions

✅ **Best Answer** - Mark the most helpful answer on your questions

✅ **Image Upload** - Add images to your questions

✅ **Study Materials** - Teachers can upload PDF resources

✅ **Search & Filter** - Find questions by subject, status, or keywords

✅ **Leaderboard** - Compete with other students

✅ **Analytics Dashboard** - View charts and statistics (Admin)

## Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `run.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Database Issues
Delete the `database` folder and run `python run.py` again to recreate.

### Upload Issues
Ensure the `static/uploads` directory has write permissions.

## Project Structure Overview

```
askbuddy/
├── run.py              # Start the application
├── app.py              # Main Flask application
├── config.py           # Configuration
├── seed_data.py        # Sample data generator
├── models/             # Database models
├── templates/          # HTML pages
├── static/             # CSS, JS, uploads
└── database/           # SQLite database (auto-created)
```

## Need Help?

- Check `README.md` for detailed documentation
- Review the code comments in `app.py`
- Examine the database schema in `models/database.py`

## Tips for Best Experience

1. **Add Sample Data** - Makes testing easier
2. **Try Different Roles** - Login as student, teacher, and admin
3. **Post Questions** - Test the similar question detection
4. **Vote on Answers** - See reputation points in action
5. **Upload Materials** - Test file upload as teacher
6. **Check Analytics** - View charts in admin dashboard

---

**Ready to start? Run:** `python run.py`

**AskBuddy - Solve Doubts Faster! 🎓**
