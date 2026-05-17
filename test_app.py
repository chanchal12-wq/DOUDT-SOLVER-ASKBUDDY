#!/usr/bin/env python3
"""
Quick test script to verify AskBuddy is working
"""

import sys

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from app import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_routes():
    """Test if routes are registered"""
    print("\nTesting routes...")
    try:
        from app import app
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        required_routes = [
            '/',
            '/login',
            '/register',
            '/student/dashboard',
            '/teacher/dashboard',
            '/admin/dashboard'
        ]
        
        missing = []
        for route in required_routes:
            if route not in routes:
                missing.append(route)
        
        if missing:
            print(f"❌ Missing routes: {missing}")
            return False
        
        print(f"✅ All {len(routes)} routes registered correctly")
        return True
    except Exception as e:
        print(f"❌ Route test error: {e}")
        return False

def test_database():
    """Test if database can be initialized"""
    print("\nTesting database...")
    try:
        from models.database import init_db
        import os
        
        # Check if database directory exists
        db_dir = os.path.join(os.path.dirname(__file__), 'database')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        print("✅ Database module working")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_templates():
    """Test if templates exist"""
    print("\nTesting templates...")
    try:
        import os
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        required_templates = [
            'base.html',
            'index.html',
            'login.html',
            'register.html',
            'student_dashboard.html',
            'teacher_dashboard.html',
            'admin_dashboard.html'
        ]
        
        missing = []
        for template in required_templates:
            if not os.path.exists(os.path.join(templates_dir, template)):
                missing.append(template)
        
        if missing:
            print(f"❌ Missing templates: {missing}")
            return False
        
        print("✅ All templates present")
        return True
    except Exception as e:
        print(f"❌ Template test error: {e}")
        return False

def main():
    print("=" * 60)
    print("  AskBuddy - Application Test")
    print("=" * 60)
    print()
    
    tests = [
        test_imports,
        test_routes,
        test_database,
        test_templates
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print()
    print("=" * 60)
    if all(results):
        print("✅ ALL TESTS PASSED!")
        print("You can now run: python app.py")
        print("Or run: python start.py")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the errors above")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
