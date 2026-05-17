#!/usr/bin/env python3
"""
AskBuddy Startup Script
This script ensures all dependencies are met before starting the application
"""

import sys
import os

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['flask', 'werkzeug']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_directories():
    """Ensure required directories exist"""
    directories = [
        'database',
        'static/uploads/questions',
        'static/uploads/materials'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return True

def main():
    print("=" * 60)
    print("  AskBuddy - Smart Student Doubt Exchange System")
    print("  Solve Doubts Faster")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed")
    print()
    
    # Check directories
    print("📁 Checking directories...")
    check_directories()
    print("✅ All directories ready")
    print()
    
    # Import and run the app
    print("🚀 Starting AskBuddy server...")
    print("📍 Server will be available at: http://localhost:5000")
    print()
    print("🔑 Default Admin Account:")
    print("   Email: admin@askbuddy.com")
    print("   Password: admin123")
    print()
    print("⏹️  Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        from app import app
        print("📍 Open: http://localhost:5000")
        print()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure port 5000 is not in use")
        print("   2. Check if all files are present")
        print("   3. Try: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped. Thank you for using AskBuddy!")
        sys.exit(0)
