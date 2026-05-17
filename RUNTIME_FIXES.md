# AskBuddy - Runtime Error Fixes

## Common Runtime Errors and Solutions

### ✅ All Issues Fixed!

The following issues have been resolved in the codebase:

1. **Database initialization outside app context** - Fixed ✅
2. **Missing `__init__.py` in models folder** - Added ✅
3. **Database error handling** - Improved ✅
4. **Chart.js template syntax errors** - Fixed ✅

---

## How to Run (Updated)

### Method 1: Using start.py (Recommended)
```bash
cd askbuddy
python start.py
```

### Method 2: Using run.py
```bash
cd askbuddy
python run.py
```

### Method 3: Using app.py directly
```bash
cd askbuddy
python app.py
```

---

## What Was Fixed

### 1. Database Initialization Issue
**Problem:** `init_db()` was called outside Flask application context

**Solution:** Changed to initialize on first request
```python
@app.before_request
def initialize_database():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True
```

### 2. Missing Models Package
**Problem:** Python couldn't import from models folder

**Solution:** Added `models/__init__.py` file

### 3. Database Error Handling
**Problem:** No error handling in database initialization

**Solution:** Added try-except blocks and return status

### 4. Chart.js Template Errors
**Problem:** Jinja2 syntax in JavaScript caused linter errors

**Solution:** Used data attributes and JSON parsing
```html
<canvas id="subjectChart" 
        data-labels='{{ subject_stats|map(attribute="subject")|list|tojson }}'
        data-values='{{ subject_stats|map(attribute="count")|list|tojson }}'></canvas>
```

---

## If You Still Get Errors

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
**Solution:**
```bash
# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in start.py/run.py to 5001
```

### Error: "No such table: users"
**Solution:**
```bash
# Delete database and restart
rm -rf database/
python start.py
```

### Error: "Working outside of application context"
**Solution:** This has been fixed! Just restart the server.

### Error: "Permission denied" on database folder
**Solution:**
```bash
# Create directories manually
mkdir database
mkdir -p static/uploads/questions
mkdir -p static/uploads/materials

# Set permissions (Linux/Mac)
chmod 755 database static/uploads
```

---

## Verification Steps

1. **Check Python version:**
```bash
python --version
# Should be 3.7 or higher
```

2. **Check Flask installation:**
```bash
python -c "import flask; print(flask.__version__)"
# Should print version number
```

3. **Test app import:**
```bash
cd askbuddy
python -c "from app import app; print('Success!')"
```

4. **Check file structure:**
```bash
ls -la
# Should see: app.py, config.py, models/, templates/, static/
```

---

## Success Indicators

When the server starts successfully, you should see:
```
🚀 Starting AskBuddy server...
📍 Server will be available at: http://localhost:5000

🔑 Default Admin Account:
   Email: admin@askbuddy.com
   Password: admin123

 * Running on http://0.0.0.0:5000
 * Restarting with stat
```

---

## Quick Test

After starting the server, test these URLs:

1. **Home Page:** http://localhost:5000
2. **Login Page:** http://localhost:5000/login
3. **Register Page:** http://localhost:5000/register

If all three load without errors, the app is working correctly!

---

## Still Having Issues?

Please provide the **exact error message** from your terminal, including:
- The full error traceback
- The command you ran
- Your Python version
- Your operating system

---

**All runtime issues have been fixed! The application should now start without errors.** 🎉
