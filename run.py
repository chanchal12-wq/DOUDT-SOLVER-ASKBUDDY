#!/usr/bin/env python3
"""
AskBuddy - Smart Student Doubt Exchange System
Run this script to start the application
"""

import os
import sys

def main():
    print("=" * 60)
    print("  AskBuddy - Smart Student Doubt Exchange System")
    print("  Solve Doubts Faster")
    print("=" * 60)
    print()
    
    # Check if database exists
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'askbuddy.db')
    
    if not os.path.exists(db_path):
        print("Database not found. Initializing...")
        from models.database import init_db
        init_db()
        print("Database initialized successfully!")
        print()
        
        # Ask if user wants to seed data
        response = input("Would you like to add sample data for testing? (y/n): ")
        if response.lower() == 'y':
            from seed_data import seed_database
            seed_database()
        print()
    
    print("Starting AskBuddy server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print()
    print("Default Admin Account:")
    print("  Email: admin@askbuddy.com")
    print("  Password: admin123")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped. Thank you for using AskBuddy!")
        sys.exit(0)
