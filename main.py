"""
Student Assistant Chatbot - Hybrid AI System
Main Entry Point

This script initializes the application and provides setup commands.
"""
import os
import sys
from app import app, db

def setup_database():
    """Initialize database and create default admin"""
    with app.app_context():
        print("🔄 Initializing database...")
        db.create_all()
        
        from models import User
        
        # Create default admin if not exists
        admin = User.query.filter_by(email='admin@university.com').first()
        if not admin:
            admin = User(
                email='admin@university.com',
                full_name='System Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Database initialized")
            print("✓ Default admin created:")
            print("  Email: admin@university.com")
            print("  Password: admin123")
            print("\n⚠️  IMPORTANT: Change admin password after first login!")
        else:
            print("✓ Database already initialized")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init-db':
            setup_database()
        else:
            print("Unknown command. Use 'init-db' to initialize database.")
    else:
        # Default: Run the app
        print("""
╔════════════════════════════════════════════════════════════════╗
║   🎓 Student Assistant Chatbot - Hybrid AI System             ║
║                                                                ║
║   📚 Features:                                                 ║
║   • Rule-based query engine for structured data               ║
║   • AI-powered responses via Groq API                         ║
║   • Admin Dashboard for data management                       ║
║   • Teacher Dashboard for content updates                     ║
║   • Secure authentication with role-based access              ║
║                                                                ║
║   🚀 Starting server...                                       ║
║   📍 Access at: http://localhost:5000                         ║
║                                                                ║
║   👨‍💼 Admin Login:                                              ║
║   Email: admin@university.com                                 ║
║   Password: admin123                                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """)
        app.run(debug=True)
