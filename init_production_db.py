#!/usr/bin/env python
"""
Production Database Initialization Script
Run this on Render to set up initial data
"""

from app import app, db, Venue, Event, User
import datetime

def init_production_database():
    """Initialize production database with sample data"""
    with app.app_context():
        print("=" * 60)
        print("Initializing Production Database")
        print("=" * 60)
        print()
        
        try:
            # Create tables
            print("Creating database tables...")
            db.create_all()
            print("✅ Tables created")
            print()
            
            # Check if data already exists
            if Venue.query.count() > 0:
                print("⚠️  Database already has data. Skipping initialization.")
                return
            
            # Create sample venues
            print("Creating sample venues...")
            venues = [
                Venue(
                    name='Grand Convention Center',
                    address='123 Main Street, Downtown',
                    city='Delhi',
                    state='Delhi',
                    zip_code='110001',
                    capacity=500
                ),
                Venue(
                    name='Tech Park Auditorium',
                    address='456 Tech Road, Cyber City',
                    city='Bangalore',
                    state='Karnataka',
                    zip_code='560001',
                    capacity=300
                ),
                Venue(
                    name='Beachside Resort',
                    address='789 Beach Road',
                    city='Mumbai',
                    state='Maharashtra',
                    zip_code='400001',
                    capacity=200
                )
            ]
            
            for venue in venues:
                db.session.add(venue)
            
            db.session.commit()
            print(f"✅ Created {len(venues)} venues")
            print()
            
            # Create sample event
            print("Creating sample event...")
            venue = Venue.query.first()
            
            event = Event(
                name='Welcome Event - EventHub Launch',
                description='Join us for the grand launch of EventHub platform!',
                date=datetime.date.today() + datetime.timedelta(days=7),
                time=datetime.time(18, 0),
                location_id=venue.venue_id
            )
            
            db.session.add(event)
            db.session.commit()
            print(f"✅ Created sample event: {event.name}")
            print()
            
            # Summary
            print("=" * 60)
            print("✅ Production Database Initialized Successfully!")
            print("=" * 60)
            print()
            print("Summary:")
            print(f"  Venues: {Venue.query.count()}")
            print(f"  Events: {Event.query.count()}")
            print(f"  Users: {User.query.count()}")
            print()
            print("You can now:")
            print("  1. Login to dashboard")
            print("  2. Create more events")
            print("  3. Manage venues")
            print()
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    init_production_database()
