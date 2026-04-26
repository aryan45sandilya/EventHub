#!/usr/bin/env python
"""
NUCLEAR OPTION: Reset and recreate entire database
"""

from app import app, db
import os

def reset_database():
    """Drop all tables and recreate from scratch"""
    with app.app_context():
        print("=" * 60)
        print("RESETTING DATABASE - NUCLEAR OPTION")
        print("=" * 60)
        print()
        
        try:
            # Drop all tables
            print("Dropping all tables...")
            db.drop_all()
            print("✅ All tables dropped")
            print()
            
            # Recreate all tables
            print("Creating all tables from scratch...")
            db.create_all()
            print("✅ All tables created")
            print()
            
            print("=" * 60)
            print("✅ Database reset complete!")
            print("=" * 60)
            print()
            print("Next steps:")
            print("1. Run: python create_admin_users.py")
            print("2. Run: python init_production_db.py")
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    reset_database()
