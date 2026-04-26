#!/usr/bin/env python
"""
Database Check Script
Checks the current state of the database and helps diagnose issues
"""

from app import app, db, Event, Venue, User, Order, Ticket, Speaker

def check_database():
    """Check database status and print statistics"""
    with app.app_context():
        print("=" * 60)
        print("EventHub Database Status Check")
        print("=" * 60)
        print()
        
        try:
            # Test connection
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection: OK")
            print()
            
            # Get counts
            print("📊 Database Statistics:")
            print("-" * 60)
            
            user_count = User.query.count()
            print(f"👥 Users: {user_count}")
            
            venue_count = Venue.query.count()
            print(f"🏛️  Venues: {venue_count}")
            
            event_count = Event.query.count()
            print(f"🎪 Events: {event_count}")
            
            speaker_count = Speaker.query.count()
            print(f"🎤 Speakers: {speaker_count}")
            
            order_count = Order.query.count()
            print(f"🛒 Orders: {order_count}")
            
            ticket_count = Ticket.query.count()
            print(f"🎟️  Tickets: {ticket_count}")
            
            print()
            
            # Check for issues
            print("🔍 Checking for Issues:")
            print("-" * 60)
            
            if venue_count == 0:
                print("⚠️  WARNING: No venues found!")
                print("   → Events cannot be created without venues")
                print("   → Solution: Create a venue first from dashboard")
                print()
            else:
                print("✅ Venues exist")
                venues = Venue.query.all()
                for v in venues:
                    print(f"   - {v.name} (ID: {v.venue_id}, City: {v.city})")
                print()
            
            if event_count == 0:
                print("ℹ️  No events found")
                if venue_count > 0:
                    print("   → You can create events now")
                print()
            else:
                print(f"✅ {event_count} event(s) found")
                events = Event.query.all()
                for e in events:
                    print(f"   - {e.name} (ID: {e.event_id}, Date: {e.date})")
                print()
            
            if user_count == 0:
                print("⚠️  WARNING: No users found!")
                print("   → Run: python create_admin_users.py")
                print()
            else:
                print(f"✅ {user_count} user(s) found")
                organizers = User.query.filter_by(user_type='organizer').count()
                attendees = User.query.filter_by(user_type='attendee').count()
                admins = User.query.filter_by(user_type='administrator').count()
                print(f"   - Administrators: {admins}")
                print(f"   - Organizers: {organizers}")
                print(f"   - Attendees: {attendees}")
                print()
            
            print("=" * 60)
            print("✅ Database check complete!")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_database()
