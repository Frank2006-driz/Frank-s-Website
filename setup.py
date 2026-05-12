"""
Setup script to initialize the database and create the first admin user.
Run this script once after installing dependencies.
"""

import sys
from app import app, db, User

def setup_database():
    """Initialize database and create tables."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")

def create_admin_user():
    """Create the first admin user."""
    with app.app_context():
        username = input("\nEnter admin username: ").strip()
        
        if User.query.filter_by(username=username).first():
            print("✗ Username already exists!")
            return False
        
        email = input("Enter admin email: ").strip()
        
        if User.query.filter_by(email=email).first():
            print("✗ Email already registered!")
            return False
        
        password = input("Enter admin password: ").strip()
        confirm_password = input("Confirm password: ").strip()
        
        if password != confirm_password:
            print("✗ Passwords do not match!")
            return False
        
        if len(password) < 6:
            print("✗ Password must be at least 6 characters!")
            return False
        
        admin_user = User(
            username=username,
            email=email,
            is_admin=True
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"✓ Admin user '{username}' created successfully!")
        return True

def create_sample_categories():
    """Create sample categories."""
    from app import Category
    
    with app.app_context():
        categories = [
            Category(name="Technology", slug="technology", description="Tech news and updates"),
            Category(name="Business", slug="business", description="Business insights and tips"),
            Category(name="Lifestyle", slug="lifestyle", description="Lifestyle and personal development"),
            Category(name="News", slug="news", description="Latest news and updates"),
            Category(name="Tutorial", slug="tutorial", description="How-to guides and tutorials"),
        ]
        
        for cat in categories:
            if not Category.query.filter_by(slug=cat.slug).first():
                db.session.add(cat)
        
        db.session.commit()
        print("✓ Sample categories created")

if __name__ == '__main__':
    try:
        print("=" * 50)
        print("Website Setup")
        print("=" * 50)
        
        # Setup database
        setup_database()
        
        # Create admin user
        print("\n--- Create Admin User ---")
        if create_admin_user():
            # Create sample categories
            print("\n--- Creating Sample Categories ---")
            create_sample_categories()
            
            print("\n" + "=" * 50)
            print("Setup complete! 🎉")
            print("=" * 50)
            print("\nYou can now run: python app.py")
            print("Then visit: http://localhost:5000")
        else:
            print("\n✗ Setup failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ Error during setup: {e}")
        sys.exit(1)
