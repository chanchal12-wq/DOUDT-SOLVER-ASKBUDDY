# AskBuddy - Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue: "pip: command not found"
**Solution:**
```bash
# Install pip first
python -m ensurepip --upgrade

# Or use python3
python3 -m pip install -r requirements.txt
```

#### Issue: "Permission denied" when installing packages
**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: "Module not found: Flask"
**Solution:**
```bash
# Ensure you're in the correct directory
cd askbuddy

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list | grep Flask
```

---

### Database Issues

#### Issue: "Database is locked"
**Solution:**
```bash
# Close all connections to the database
# Stop the Flask server (Ctrl+C)
# Delete the database file
rm database/askbuddy.db

# Restart the application
python run.py
```

#### Issue: "Table does not exist"
**Solution:**
```bash
# Delete and recreate database
rm -rf database/
python run.py
# Select 'y' when asked to add sample data
```

#### Issue: "Integrity error: UNIQUE constraint failed"
**Solution:**
- This means you're trying to create a duplicate entry
- For users: Email already exists
- For votes: User already voted on this answer
- Check if the record already exists before creating

---

### Server Issues

#### Issue: "Address already in use" (Port 5000 busy)
**Solution 1:** Kill the process using port 5000
```bash
# On Linux/Mac
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution 2:** Change the port in `run.py`
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001
```

#### Issue: "Connection refused" when accessing localhost
**Solution:**
- Ensure the server is running
- Check if you're using the correct URL: http://localhost:5000
- Try http://127.0.0.1:5000 instead
- Check firewall settings

#### Issue: Server crashes immediately after starting
**Solution:**
```bash
# Check for syntax errors
python -m py_compile app.py

# Run with verbose error messages
python -u run.py

# Check Python version (requires 3.7+)
python --version
```

---

### Login & Authentication Issues

#### Issue: "Invalid email or password" with correct credentials
**Solution:**
- Ensure database is initialized
- Check if user exists in database
- Try creating a new account
- Use default admin: admin@askbuddy.com / admin123

#### Issue: "Session expired" or logged out unexpectedly
**Solution:**
- Check if SECRET_KEY is set in config.py
- Clear browser cookies
- Restart the server
- Check browser console for errors

#### Issue: Can't access certain pages (403 Forbidden)
**Solution:**
- Verify you're logged in
- Check your user role (student/teacher/admin)
- Some pages are role-restricted
- Try logging out and back in

---

### File Upload Issues

#### Issue: "File too large" error
**Solution:**
- Check file size (max 16MB)
- Reduce image size before uploading
- Compress PDF files
- Modify MAX_CONTENT_LENGTH in config.py if needed

#### Issue: Uploaded files not appearing
**Solution:**
```bash
# Check if upload directories exist
ls -la static/uploads/questions/
ls -la static/uploads/materials/

# Create directories if missing
mkdir -p static/uploads/questions
mkdir -p static/uploads/materials

# Check permissions
chmod 755 static/uploads/
```

#### Issue: "Invalid file type" error
**Solution:**
- For questions: Use PNG, JPG, JPEG, or GIF
- For materials: Use PDF only
- Check file extension is correct
- Rename file if it has special characters

---

### UI/Display Issues

#### Issue: Page looks broken or unstyled
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for errors (F12)
- Verify static files are loading
- Try a different browser
- Check internet connection (Bootstrap CDN)

#### Issue: Charts not displaying
**Solution:**
- Ensure Chart.js is loading (check browser console)
- Verify data is being passed to template
- Check JavaScript console for errors
- Try refreshing the page

#### Issue: Images not displaying
**Solution:**
- Check if image file exists in uploads folder
- Verify file path in database
- Check file permissions
- Try uploading image again

---

### Search & Filter Issues

#### Issue: Search returns no results
**Solution:**
- Check if questions exist in database
- Try broader search terms
- Remove filters and try again
- Check for typos in search query

#### Issue: Similar questions not appearing
**Solution:**
- Type at least 3 characters in title
- Wait 1 second for suggestions to load
- Check browser console for errors
- Verify API endpoint is working

---

### Reputation & Voting Issues

#### Issue: Reputation points not updating
**Solution:**
- Refresh the page
- Log out and log back in
- Check database for correct values
- Verify voting logic in code

#### Issue: Can't vote on answers
**Solution:**
- Ensure you're logged in
- Can't vote on your own answers
- Check if you already voted
- Verify JavaScript is enabled

#### Issue: Can't mark best answer
**Solution:**
- Must be question author or teacher
- Question must not already be solved
- Only one best answer per question
- Refresh page and try again

---

### Performance Issues

#### Issue: Slow page loading
**Solution:**
- Check database size
- Optimize images before uploading
- Clear browser cache
- Restart the server
- Consider pagination for large datasets

#### Issue: Database growing too large
**Solution:**
```bash
# Backup database
cp database/askbuddy.db database/askbuddy_backup.db

# Clean up old data (optional)
# Delete old questions, answers, etc.

# Optimize database
sqlite3 database/askbuddy.db "VACUUM;"
```

---

### Development Issues

#### Issue: Changes not reflecting
**Solution:**
- Restart Flask server (Ctrl+C, then python run.py)
- Clear browser cache
- Check if you're editing the correct file
- Verify file is saved

#### Issue: Template not found error
**Solution:**
- Check template name spelling
- Verify file exists in templates/ folder
- Check file extension (.html)
- Restart server

#### Issue: Static files not loading
**Solution:**
- Check file path in template
- Verify file exists in static/ folder
- Clear browser cache
- Use url_for() in templates

---

### Browser-Specific Issues

#### Chrome Issues
- Clear cache: Ctrl+Shift+Delete
- Disable extensions
- Try incognito mode
- Check console (F12)

#### Firefox Issues
- Clear cache: Ctrl+Shift+Delete
- Disable add-ons
- Try private window
- Check console (F12)

#### Safari Issues
- Clear cache: Cmd+Option+E
- Enable developer tools
- Check console
- Try different browser

---

### Error Messages

#### "Internal Server Error (500)"
**Causes:**
- Syntax error in Python code
- Database connection issue
- Missing file or directory
- Unhandled exception

**Solution:**
- Check terminal for error details
- Review recent code changes
- Check file permissions
- Restart server

#### "Not Found (404)"
**Causes:**
- Incorrect URL
- Route not defined
- Template missing

**Solution:**
- Check URL spelling
- Verify route exists in app.py
- Check template name

#### "Bad Request (400)"
**Causes:**
- Missing form data
- Invalid input
- CSRF token issue

**Solution:**
- Check form fields
- Verify all required fields filled
- Clear cookies and try again

---

### Data Issues

#### Issue: Sample data not loading
**Solution:**
```bash
# Run seed script manually
python seed_data.py

# Or delete database and restart
rm -rf database/
python run.py
# Select 'y' for sample data
```

#### Issue: Duplicate data appearing
**Solution:**
- Don't run seed_data.py multiple times
- Check for duplicate entries in database
- Delete database and recreate

---

### Security Issues

#### Issue: "CSRF token missing"
**Solution:**
- Ensure forms include CSRF token
- Check if session is active
- Clear cookies
- Restart server

#### Issue: Can't upload files
**Solution:**
- Check form has enctype="multipart/form-data"
- Verify file input name matches backend
- Check file size and type
- Review upload permissions

---

## Debugging Tips

### Enable Debug Mode
Already enabled in development. Check terminal for detailed errors.

### Check Logs
```bash
# View server output
python run.py

# All errors appear in terminal
```

### Database Inspection
```bash
# Open database
sqlite3 database/askbuddy.db

# List tables
.tables

# View users
SELECT * FROM users;

# View questions
SELECT * FROM questions;

# Exit
.quit
```

### Browser Developer Tools
- Press F12 to open
- Check Console tab for JavaScript errors
- Check Network tab for failed requests
- Check Application tab for cookies/session

---

## Getting Help

### Before Asking for Help

1. Check this troubleshooting guide
2. Review error messages carefully
3. Check browser console (F12)
4. Try restarting the server
5. Try a different browser

### Information to Provide

When reporting issues, include:
- Error message (full text)
- Steps to reproduce
- Browser and version
- Operating system
- Python version
- What you've already tried

### Useful Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Flask installation
python -c "import flask; print(flask.__version__)"

# Test database connection
python -c "import sqlite3; print('SQLite OK')"

# Check file permissions
ls -la database/
ls -la static/uploads/
```

---

## Reset Everything

If all else fails, start fresh:

```bash
# 1. Stop the server (Ctrl+C)

# 2. Delete database
rm -rf database/

# 3. Delete uploaded files
rm -rf static/uploads/questions/*
rm -rf static/uploads/materials/*

# 4. Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# 5. Restart
python run.py

# 6. Add sample data when prompted
```

---

## Still Having Issues?

1. Review the README.md for setup instructions
2. Check QUICKSTART.md for basic usage
3. Review code comments in app.py
4. Check database schema in models/database.py
5. Verify all files are present (see PROJECT_SUMMARY.md)

---

**Remember:** Most issues can be solved by restarting the server and clearing browser cache!
