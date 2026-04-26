import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import bcrypt
from functools import wraps
from typing import List
import datetime
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'eventhub.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.jinja_env.bytecode_cache = None

# Configure logging for production
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/eventhub.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('EventHub startup')

# Force no-cache on all responses so browser never serves stale pages
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Add context processor for current year
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# Global error handlers
@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    db.session.rollback()
    app.logger.error(f'Server Error: {error}', exc_info=True)
    flash('An internal error occurred. Please try again later.', 'danger')
    return render_template('index.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('index.html'), 404

# --- Database Models ---
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.Enum('organizer', 'attendee', 'administrator'), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    events = db.relationship('Event', backref='venue', lazy=True)

class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)  # Keep the old time field for now
    location_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False)
    speakers = db.relationship('Speaker', backref='event', lazy=True)
    tickets = db.relationship('Ticket', backref='event', lazy=True)
    
    # Properties to handle time information
    _start_time = None
    _end_time = None
    
    @property
    def start_time(self):
        if self._start_time is not None:
            return self._start_time
        elif self.time is not None:
            return self.time
        return None
    
    @start_time.setter
    def start_time(self, value):
        if isinstance(value, str):
            self._start_time = datetime.datetime.strptime(value, '%H:%M').time()
        else:
            self._start_time = value
    
    @property
    def end_time(self):
        if self._end_time is not None:
            return self._end_time
        elif self.time is not None:
            # If we only have the old time field, use it as both start and end
            return self.time
        return None
    
    @end_time.setter
    def end_time(self, value):
        if isinstance(value, str):
            self._end_time = datetime.datetime.strptime(value, '%H:%M').time()
        else:
            self._end_time = value

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'))
    tickets = db.relationship('Ticket', backref='order', lazy=True)
    payment = db.relationship('Payment', backref=db.backref('order', uselist=False), foreign_keys=[payment_id])

class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False, unique=True)
    payment_method = db.Column(db.Enum('credit card', 'paypal', 'other'), nullable=False)
    transaction_id = db.Column(db.String(255))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id   = db.Column(db.Integer, primary_key=True)
    event_id    = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    order_id    = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    type        = db.Column(db.String(50), nullable=False)
    seat_number = db.Column(db.Integer)
    qr_token    = db.Column(db.String(64), unique=True)   # unique token for QR
    checked_in  = db.Column(db.Boolean, default=False)
    checked_in_at = db.Column(db.DateTime, nullable=True)
    short_code  = db.Column(db.String(12), unique=True)   # e.g. EVT-A3K9

class Speaker(db.Model):
    __tablename__ = 'speaker'
    speaker_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

class TicketType(db.Model):
    __tablename__ = 'tickettype'
    ticket_type_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    event = db.relationship('Event', backref=db.backref('ticket_types', lazy=True))

class Reminder(db.Model):
    __tablename__ = 'reminder'
    reminder_id = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    event_id    = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    remind_at   = db.Column(db.DateTime, nullable=False)
    method      = db.Column(db.String(20), default='email')   # email / sms
    message     = db.Column(db.Text)
    sent        = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.datetime.now)
    user  = db.relationship('User',  backref='reminders')
    event = db.relationship('Event', backref='reminders')

# --- Helper Functions ---
def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    """Checks if the provided password matches the hashed password."""
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def generate_qr_image(data: str) -> str:
    """Generate a QR code and return as base64 PNG string."""
    import qrcode, io, base64
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="#ffffff")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_short_code() -> str:
    """Generate a short human-readable ticket code like EVT-A3K9."""
    import random, string
    chars = string.ascii_uppercase + string.digits
    # Remove confusing chars: 0,O,I,1,L
    chars = chars.translate(str.maketrans('', '', '0OI1L'))
    part = ''.join(random.choices(chars, k=4))
    return f'EVT-{part}'

# --- Decorators ---
def login_required(role="attendee"):
    """Decorator to require login and specific role."""
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('login'))
            
            # Administrator has access to everything
            if user.user_type == 'administrator':
                return f(*args, **kwargs)
                
            # For non-administrators, check role
            if user.user_type != role:
                if user.user_type == 'organizer' and role == 'attendee':
                    pass  # Allow organizer to see attendee views
                else:
                    flash('You do not have permission to access this page.', 'danger')
                    return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def organizer_required(f):
     """Simplified decorator for organizer role."""
     return login_required(role="organizer")(f)


# --- Routes ---
@app.route('/')
def index():
    """Home page displaying upcoming events."""
    events = Event.query.order_by(Event.date.asc()).limit(6).all() # Show upcoming events
    return render_template('index.html', events=events)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    from flask import jsonify
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.datetime.now().isoformat()
        }), 200
    except Exception as e:
        app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@app.route('/events')
def list_events():
    """Page displaying all events."""
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@app.route('/events/<int:event_id>')
def event_details(event_id):
    """Page displaying details for a specific event."""
    event = Event.query.get_or_404(event_id)
    ticket_types = TicketType.query.filter_by(event_id=event_id).all()
    
    # Set time information from form data if available
    if request.args.get('start_time'):
        event.start_time = request.args.get('start_time')
    if request.args.get('end_time'):
        event.end_time = request.args.get('end_time')
    
    return render_template('event_details.html', event=event, ticket_types=ticket_types)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if 'user_id' in session:
        return redirect(url_for('index')) # Already logged in

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password(user.password, password):
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            session['user_role'] = user.user_type
            flash('Login successful!', 'success')
            if user.user_type == 'organizer':
                 return redirect(url_for('dashboard'))
            else:
                 return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user registration."""
    if 'user_id' in session:
        return redirect(url_for('index')) # Already logged in

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')

        hashed_pw = hash_password(password)

        new_user = User(name=name, email=email, password=hashed_pw, user_type=user_type)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email address already exists.', 'danger')
        except Exception as e:
             db.session.rollback()
             flash(f'An error occurred: {e}', 'danger')


    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Logs the user out."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# --- Organizer Routes (Require 'organizer' role) ---
@app.route('/dashboard')
@organizer_required
def dashboard():
    """Organizer dashboard."""
    try:
        # Ensure database tables exist
        db.create_all()
        
        # Fetch data relevant to the organizer with eager loading to avoid N+1 queries
        events = Event.query.options(
            db.joinedload(Event.venue)
        ).order_by(Event.date.asc()).all()
        
        venues = Venue.query.all()
        speakers = Speaker.query.options(db.joinedload(Speaker.event)).all()
        tickets = Ticket.query.all()
        
        # Eager load user relationship to prevent lazy loading issues
        orders = Order.query.options(
            db.joinedload(Order.user)
        ).order_by(Order.date.desc()).all()

        return render_template('dashboard.html',
                               events=events,
                               venues=venues,
                               speakers=speakers,
                               tickets=tickets,
                               orders=orders)
    except Exception as e:
        app.logger.error(f"Dashboard error: {str(e)}", exc_info=True)
        flash('An error occurred while loading the dashboard. Please try again.', 'danger')
        return render_template('dashboard.html',
                               events=[],
                               venues=[],
                               speakers=[],
                               tickets=[],
                               orders=[])


# --- CRUD Operations for Events (Organizer Only) ---

@app.route('/events/create', methods=['GET', 'POST'])
@organizer_required
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        date = datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        location_id = request.form.get('location_id')
        speaker_ids = request.form.getlist('speakers')

        # Create event with the old time field for backward compatibility
        event = Event(
            name=name,
            description=description,
            date=date,
            time=datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None,
            location_id=location_id
        )

        # Set the new time properties
        event.start_time = start_time
        event.end_time = end_time

        # Add selected speakers
        for speaker_id in speaker_ids:
            speaker = Speaker.query.get(speaker_id)
            if speaker:
                event.speakers.append(speaker)

        try:
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating event. Please try again.', 'error')
            app.logger.error(f"Error creating event: {str(e)}")

    venues = Venue.query.all()
    speakers = Speaker.query.all()
    return render_template('event_form.html', form_title='Create Event', form_action=url_for('create_event'), venues=venues, all_speakers=speakers)


@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@organizer_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.name = request.form.get('name')
        event.description = request.form.get('description')
        event.date = datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        
        # Update the old time field
        start_time = request.form.get('start_time')
        if start_time:
            event.time = datetime.datetime.strptime(start_time, '%H:%M').time()
        
        # Update the new time properties
        event.start_time = start_time
        event.end_time = request.form.get('end_time')
        
        event.location_id = request.form.get('location_id')
        
        # Update speakers
        event.speakers = []
        for speaker_id in request.form.getlist('speakers'):
            speaker = Speaker.query.get(speaker_id)
            if speaker:
                event.speakers.append(speaker)

        try:
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating event. Please try again.', 'error')
            app.logger.error(f"Error updating event: {str(e)}")

    venues = Venue.query.all()
    speakers = Speaker.query.all()
    return render_template('event_form.html', form_title='Edit Event', form_action=url_for('edit_event', event_id=event_id), event=event, venues=venues, all_speakers=speakers)


@app.route('/events/<int:event_id>/delete', methods=['POST'])
@organizer_required
def delete_event(event_id):
    """Delete an event."""
    event = Event.query.get_or_404(event_id)
    try:
        # Manually delete related Speakers and Tickets if cascade doesn't work as expected
        # Speaker.query.filter_by(event_id=event_id).delete()
        # Ticket.query.filter_by(event_id=event_id).delete()
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {e}', 'danger')
    return redirect(url_for('dashboard'))


# --- CRUD Operations for Venues (Organizer Only) ---

@app.route('/venues/create', methods=['GET', 'POST'])
@organizer_required
def create_venue():
     if request.method == 'POST':
        name = request.form['name']
        address = request.form.get('address')
        capacity = request.form.get('capacity', type=int)
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        new_venue = Venue(name=name, address=address, capacity=capacity, city=city, state=state, zip_code=zip_code)
        try:
             db.session.add(new_venue)
             db.session.commit()
             flash('Venue created successfully!', 'success')
             return redirect(url_for('dashboard'))
        except Exception as e:
             db.session.rollback()
             flash(f'Error creating venue: {e}', 'danger')
     return render_template('venue_form.html', form_action=url_for('create_venue'), form_title="Create New Venue")


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
@organizer_required
def edit_venue(venue_id):
     venue = Venue.query.get_or_404(venue_id)
     if request.method == 'POST':
         venue.name = request.form['name']
         venue.address = request.form.get('address')
         venue.capacity = request.form.get('capacity', type=int)
         venue.city = request.form.get('city')
         venue.state = request.form.get('state')
         venue.zip_code = request.form.get('zip_code')
         try:
             db.session.commit()
             flash('Venue updated successfully!', 'success')
             return redirect(url_for('dashboard'))
         except Exception as e:
             db.session.rollback()
             flash(f'Error updating venue: {e}', 'danger')
     return render_template('venue_form.html', venue=venue, form_action=url_for('edit_venue', venue_id=venue_id), form_title="Edit Venue")


@app.route('/venues/<int:venue_id>/delete', methods=['POST'])
@organizer_required
def delete_venue(venue_id):
     venue = Venue.query.get_or_404(venue_id)
     if venue.events: # Check if venue is linked to events
          flash('Cannot delete venue. It is linked to existing events.', 'danger')
          return redirect(url_for('dashboard'))
     try:
         db.session.delete(venue)
         db.session.commit()
         flash('Venue deleted successfully!', 'success')
     except Exception as e:
         db.session.rollback()
         flash(f'Error deleting venue: {e}', 'danger')
     return redirect(url_for('dashboard'))


# --- CRUD Operations for Speakers (Organizer Only) ---

@app.route('/speakers/create', methods=['GET', 'POST'])
@organizer_required
def create_speaker():
     events = Event.query.order_by(Event.name).all()
     if request.method == 'POST':
         name = request.form['name']
         bio = request.form.get('bio')
         event_id = request.form['event_id']
         new_speaker = Speaker(name=name, bio=bio, event_id=event_id)
         try:
             db.session.add(new_speaker)
             db.session.commit()
             flash('Speaker created successfully!', 'success')
             return redirect(url_for('dashboard'))
         except Exception as e:
             db.session.rollback()
             flash(f'Error creating speaker: {e}', 'danger')
     return render_template('speaker_form.html', events=events, form_action=url_for('create_speaker'), form_title="Add New Speaker")


@app.route('/speakers/<int:speaker_id>/edit', methods=['GET', 'POST'])
@organizer_required
def edit_speaker(speaker_id):
     speaker = Speaker.query.get_or_404(speaker_id)
     events = Event.query.order_by(Event.name).all()
     if request.method == 'POST':
         speaker.name = request.form['name']
         speaker.bio = request.form.get('bio')
         speaker.event_id = request.form['event_id']
         try:
             db.session.commit()
             flash('Speaker updated successfully!', 'success')
             return redirect(url_for('dashboard'))
         except Exception as e:
             db.session.rollback()
             flash(f'Error updating speaker: {e}', 'danger')
     return render_template('speaker_form.html', speaker=speaker, events=events, form_action=url_for('edit_speaker', speaker_id=speaker_id), form_title="Edit Speaker")


@app.route('/speakers/<int:speaker_id>/delete', methods=['POST'])
@organizer_required
def delete_speaker(speaker_id):
     speaker = Speaker.query.get_or_404(speaker_id)
     try:
         db.session.delete(speaker)
         db.session.commit()
         flash('Speaker deleted successfully!', 'success')
     except Exception as e:
         db.session.rollback()
         flash(f'Error deleting speaker: {e}', 'danger')
     return redirect(url_for('dashboard'))


# --- CRUD Operations for Tickets (Conceptual - Booking is attendee, managing is organizer) ---
# Note: Full ticket CRUD might be complex. Organizer might manage ticket *types* per event.

@app.route('/events/<int:event_id>/tickets/manage', methods=['GET', 'POST'])
@organizer_required
def manage_event_tickets(event_id):
    """Manage ticket types for an event."""
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        ticket_type = request.form['type']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        # Calculate total tickets including existing ones
        existing_tickets = TicketType.query.filter_by(event_id=event_id).all()
        total_tickets = sum(t.quantity for t in existing_tickets) + quantity

        # Check if total tickets exceed venue capacity
        if total_tickets > event.venue.capacity:
            flash(f'Total tickets ({total_tickets}) cannot exceed venue capacity ({event.venue.capacity}).', 'danger')
            return redirect(url_for('manage_event_tickets', event_id=event_id))

        new_ticket_type = TicketType(
            event_id=event_id,
            type=ticket_type,
            price=price,
            quantity=quantity
        )

        try:
            db.session.add(new_ticket_type)
            db.session.commit()
            flash('Ticket type added successfully!', 'success')
            return redirect(url_for('manage_event_tickets', event_id=event_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding ticket type: {str(e)}', 'danger')

    ticket_types = TicketType.query.filter_by(event_id=event_id).all()
    return render_template('manage_tickets.html', event=event, ticket_types=ticket_types)

@app.route('/events/<int:event_id>/tickets')
@login_required(role="organizer")
def view_event_tickets(event_id):
    """View all tickets for an event (organizers and admins only)"""
    try:
        event = Event.query.get_or_404(event_id)
        # Get all tickets for this event with user and order information eagerly loaded
        tickets = Ticket.query.options(
            db.joinedload(Ticket.order).joinedload(Order.user),
            db.joinedload(Ticket.event)
        ).filter(Ticket.event_id == event_id).all()
        return render_template('event_tickets.html', event=event, tickets=tickets)
    except Exception as e:
        app.logger.error(f"View event tickets error: {str(e)}", exc_info=True)
        flash('An error occurred while loading tickets.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/tickets/<int:ticket_id>/delete', methods=['POST'])
@login_required(role="organizer")
def delete_ticket(ticket_id):
    """Delete a ticket type."""
    ticket_type = TicketType.query.get_or_404(ticket_id)
    event_id = ticket_type.event_id
    
    try:
        # Delete associated tickets first
        Ticket.query.filter_by(event_id=event_id, type=ticket_type.type).delete()
        db.session.delete(ticket_type)
        db.session.commit()
        flash('Ticket type deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ticket type: {str(e)}', 'danger')
    
    return redirect(url_for('manage_event_tickets', event_id=event_id))

@app.route('/tickets/<int:ticket_id>/cancel', methods=['POST'])
@login_required(role="attendee")
def cancel_ticket(ticket_id):
    """Cancel a ticket (attendees only)"""
    # Get the ticket and verify ownership
    ticket = Ticket.query.get_or_404(ticket_id)
    order = ticket.order
    
    # Check if the ticket belongs to the current user
    if order.user_id != session['user_id']:
        flash('You do not have permission to cancel this ticket.', 'danger')
        return redirect(url_for('my_tickets'))
    
    try:
        # Start a new transaction
        db.session.begin_nested()
        
        # Increment the ticket type quantity
        ticket_type = TicketType.query.filter_by(
            event_id=ticket.event_id,
            type=ticket.type
        ).first()
        if ticket_type:
            ticket_type.quantity += 1
        
        # Get the order and all its tickets
        order_id = ticket.order_id
        event_id = ticket.event_id
        ticket_type_name = ticket.type
        
        # Delete the specific ticket
        db.session.delete(ticket)
        db.session.flush()  # Flush to ensure the ticket is deleted
        
        # Check if there are any remaining tickets in the order
        remaining_tickets = Ticket.query.filter_by(order_id=order_id).all()
        
        if not remaining_tickets:
            # If no tickets remain, delete the order
            order = Order.query.get(order_id)
            if order:
                db.session.delete(order)
        else:
            # Update the order total price
            order = Order.query.get(order_id)
            if order:
                new_total = sum(float(t.price) for t in remaining_tickets)
                order.total_price = new_total
        
        # Commit the transaction
        db.session.commit()
        flash('Ticket cancelled successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling ticket: {str(e)}', 'danger')
    
    return redirect(url_for('my_tickets'))

# --- Attendee Actions ---
@app.route('/book_ticket/<int:event_id>', methods=['POST'])
def book_ticket(event_id):
    if 'user_id' not in session or session.get('user_role') != 'attendee':
        flash('Please login as an attendee to book tickets.', 'danger')
        return redirect(url_for('login'))

    event = Event.query.get_or_404(event_id)
    ticket_type_name = request.form.get('ticket_type')
    quantity = int(request.form.get('quantity', 1))
    payment_method = request.form.get('payment_method', 'other')

    ticket_type = TicketType.query.filter_by(
        event_id=event_id,
        type=ticket_type_name
    ).first()

    if not ticket_type or quantity < 1 or quantity > ticket_type.quantity:
        flash('Invalid ticket selection or not enough tickets available.', 'danger')
        return redirect(url_for('event_details', event_id=event_id))

    try:
        import uuid
        # Step 1: Create order
        order = Order(
            user_id=session['user_id'],
            date=datetime.datetime.now(),
            total_price=ticket_type.price * quantity
        )
        db.session.add(order)
        db.session.flush()  # Get order_id

        # Step 2: Create tickets
        for _ in range(quantity):
            import uuid as _uuid
            token = _uuid.uuid4().hex  # unique 32-char token
            # Generate unique short code
            sc = generate_short_code()
            while Ticket.query.filter_by(short_code=sc).first():
                sc = generate_short_code()
            ticket = Ticket(
                event_id=event_id,
                order_id=order.order_id,
                price=ticket_type.price,
                type=ticket_type.type,
                qr_token=token,
                short_code=sc
            )
            db.session.add(ticket)

        # Step 3: Reduce available quantity
        ticket_type.quantity -= quantity
        db.session.flush()

        # Step 4: Create payment
        payment = Payment(
            order_id=order.order_id,
            payment_method=payment_method,
            transaction_id=str(uuid.uuid4())[:12].upper()
        )
        db.session.add(payment)
        db.session.flush()

        # Step 5: Link payment back to order
        order.payment_id = payment.payment_id

        db.session.commit()
        flash(f'Successfully booked {quantity} {ticket_type.type} ticket(s)! Payment via {payment_method.title()}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while booking tickets.', 'danger')
        app.logger.error(f"Booking error: {str(e)}", exc_info=True)
        app.logger.error(f"Error booking tickets: {str(e)}")

    return redirect(url_for('my_tickets'))

@app.route('/my-tickets')
@login_required(role="attendee")
def my_tickets():
     """Displays tickets booked by the current attendee."""
     try:
         user_id = session['user_id']
         # Fetch orders with all necessary relationships eagerly loaded
         orders = Order.query.filter_by(user_id=user_id).options(
             db.joinedload(Order.tickets).joinedload(Ticket.event).joinedload(Event.venue),
             db.joinedload(Order.payment)
         ).order_by(Order.date.desc()).all()
         return render_template('my_tickets.html', orders=orders)
     except Exception as e:
         app.logger.error(f"My tickets error: {str(e)}", exc_info=True)
         flash('An error occurred while loading your tickets. Please try again.', 'danger')
         return render_template('my_tickets.html', orders=[])

@app.route('/orders/<int:order_id>/pay', methods=['POST'])
@login_required(role="attendee")
def complete_payment(order_id):
    """Add payment to an existing unpaid order."""
    import uuid
    order = Order.query.get_or_404(order_id)
    if order.user_id != session['user_id']:
        flash('Access denied.', 'danger')
        return redirect(url_for('my_tickets'))
    if order.payment:
        flash('This order already has a payment.', 'info')
        return redirect(url_for('my_tickets'))
    payment_method = request.form.get('payment_method', 'other')
    try:
        import uuid
        payment = Payment(
            order_id=order.order_id,
            payment_method=payment_method,
            transaction_id=str(uuid.uuid4())[:12].upper()
        )
        db.session.add(payment)
        db.session.flush()
        order.payment_id = payment.payment_id
        db.session.commit()
        flash(f'Payment completed via {payment_method.title()}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Payment failed: {e}', 'danger')
    return redirect(url_for('my_tickets'))

@app.route('/admin/organizers')
@login_required(role="administrator")
def manage_organizers():
    """Administrator view to manage organizers."""
    organizers = User.query.filter_by(user_type='organizer').all()
    return render_template('manage_organizers.html', organizers=organizers)

@app.route('/admin/organizers/<int:user_id>/delete', methods=['POST'])
@login_required(role="administrator")
def delete_organizer(user_id):
    """Delete an organizer (admin only)."""
    organizer = User.query.get_or_404(user_id)
    if organizer.user_type != 'organizer':
        flash('User is not an organizer.', 'danger')
        return redirect(url_for('manage_organizers'))
    
    try:
        # Delete associated events and tickets
        events = Event.query.filter_by(organizer_id=user_id).all()
        for event in events:
            # Delete associated tickets
            Ticket.query.filter_by(event_id=event.event_id).delete()
            # Delete ticket types
            TicketType.query.filter_by(event_id=event.event_id).delete()
            # Delete speakers
            Speaker.query.filter_by(event_id=event.event_id).delete()
            # Delete the event
            db.session.delete(event)
        
        # Delete the organizer
        db.session.delete(organizer)
        db.session.commit()
        flash('Organizer and all associated data deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting organizer: {str(e)}', 'danger')
    
    return redirect(url_for('manage_organizers'))

# --- Main Execution ---

# ── Digital Pass & QR Entry ──

@app.route('/tickets/<int:ticket_id>/pass')
@login_required(role="attendee")
def digital_pass(ticket_id):
    """Show the digital pass with QR code for a ticket."""
    try:
        ticket = Ticket.query.options(
            db.joinedload(Ticket.order).joinedload(Order.user),
            db.joinedload(Ticket.event).joinedload(Event.venue)
        ).get_or_404(ticket_id)
        
        if ticket.order.user_id != session['user_id']:
            flash('Access denied.', 'danger')
            return redirect(url_for('my_tickets'))
        
        if not ticket.qr_token:
            import uuid as _uuid
            ticket.qr_token = _uuid.uuid4().hex
            db.session.commit()
        
        if not ticket.short_code:
            ticket.short_code = generate_short_code()
            db.session.commit()
        
        qr_data = request.host_url.rstrip('/') + url_for('verify_ticket', token=ticket.qr_token)
        qr_b64  = generate_qr_image(qr_data)
        return render_template('digital_pass.html', ticket=ticket, qr_b64=qr_b64, qr_data=qr_data)
    except Exception as e:
        app.logger.error(f"Digital pass error: {str(e)}", exc_info=True)
        flash('An error occurred while loading your pass.', 'danger')
        return redirect(url_for('my_tickets'))


@app.route('/tickets/<int:ticket_id>/pass/download')
@login_required(role="attendee")
def download_pass(ticket_id):
    """Generate and serve the pass as a downloadable PNG image."""
    try:
        from flask import send_file
        import io, qrcode
        from PIL import Image, ImageDraw, ImageFont

        ticket = Ticket.query.options(
            db.joinedload(Ticket.order).joinedload(Order.user),
            db.joinedload(Ticket.event).joinedload(Event.venue)
        ).get_or_404(ticket_id)
        
        if ticket.order.user_id != session['user_id']:
            flash('Access denied.', 'danger')
            return redirect(url_for('my_tickets'))

        # ── Constants ──
        W, H    = 800, 1000
        PURPLE  = (108, 99, 255)
        DARK    = (26,  16,  64)
        DARKER  = (13,  11,  30)
        WHITE   = (255, 255, 255)
        MUTED   = (136, 146, 170)
        GREEN   = (34,  197,  94)
        LAVENDER= (167, 139, 250)
        PINK    = (236,  72, 153)

        # ── Fonts (absolute paths — fast, no search) ──
        BASE = 'C:/Windows/Fonts/'
        def fnt(name, size):
            try:    return ImageFont.truetype(BASE + name, size)
            except: return ImageFont.load_default()

        f_title  = fnt('arialbd.ttf', 36)
        f_med    = fnt('arial.ttf',   24)
        f_sm     = fnt('arial.ttf',   18)
        f_xs     = fnt('arial.ttf',   14)
        f_mono   = fnt('consola.ttf', 44)
        f_mono_s = fnt('consola.ttf', 16)

        # ── Canvas ──
        img  = Image.new('RGB', (W, H), DARKER)
        draw = ImageDraw.Draw(img)

        # ── Header — single gradient using two rectangles blended ──
        header_h = 200
        grad = Image.new('RGB', (W, header_h))
        gd   = ImageDraw.Draw(grad)
        for x in range(W):
            t = x / W
            r = int(108 + (236-108)*t)
            g = int(99  + (72 -99 )*t)
            b = int(255 + (153-255)*t)
            gd.line([(x,0),(x,header_h)], fill=(r,g,b))
        img.paste(grad, (0, 0))

        # ── Header text ──
        draw.text((36, 22),  "DIGITAL EVENT PASS", font=f_xs, fill=(255,255,255,180))
        name = ticket.event.name[:38]
        draw.text((36, 44),  name, font=f_title, fill=WHITE)
        date_str = ticket.event.date.strftime('%A, %B %d, %Y')
        if ticket.event.start_time:
            date_str += '  ·  ' + ticket.event.start_time.strftime('%I:%M %p')
        draw.text((36, 96),  date_str, font=f_sm, fill=(255,255,255,200))
        draw.text((36, 128), f"{ticket.event.venue.name}, {ticket.event.venue.city}", font=f_sm, fill=(255,255,255,160))

        # ── Dashed separator ──
        y_sep = header_h + 10
        for x in range(0, W, 18):
            draw.rectangle([(x, y_sep), (x+9, y_sep+2)], fill=(80,70,120))

        # ── Details grid ──
        fields = [
            ("ATTENDEE",    ticket.order.user.name[:28]),
            ("TICKET TYPE", ticket.type.title()),
            ("TICKET ID",   f"#{ticket.ticket_id:06d}"),
            ("PRICE PAID",  f"Rs. {float(ticket.price):.2f}"),
        ]
        col_w = W // 2
        for idx, (label, value) in enumerate(fields):
            col = idx % 2
            row = idx // 2
            x = 36 + col * col_w
            y = y_sep + 20 + row * 72
            draw.text((x, y),      label, font=f_xs,  fill=MUTED)
            draw.text((x, y + 20), value, font=f_med,  fill=WHITE)

        # ── QR Code ──
        qr_data = request.host_url.rstrip('/') + url_for('verify_ticket', token=ticket.qr_token)
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=7, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img  = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_size = 220
        qr_img  = qr_img.resize((qr_size, qr_size), Image.NEAREST)

        qr_x = (W - qr_size) // 2
        qr_y = y_sep + 20 + 2*72 + 20
        # White bg for QR
        draw.rounded_rectangle([(qr_x-14, qr_y-14), (qr_x+qr_size+14, qr_y+qr_size+14)], radius=14, fill=WHITE)
        img.paste(qr_img, (qr_x, qr_y))
        draw.text((W//2, qr_y+qr_size+22), "Scan at entry gate", font=f_sm, fill=MUTED, anchor="mm")

        # ── Short code box ──
        sc_y  = qr_y + qr_size + 52
        bw, bh = 360, 90
        bx    = (W - bw) // 2
        draw.rounded_rectangle([(bx, sc_y), (bx+bw, sc_y+bh)], radius=12, fill=(40,30,80), outline=PURPLE, width=2)
        draw.text((W//2, sc_y+14), "MANUAL ENTRY CODE", font=f_xs,   fill=MUTED,    anchor="mm")
        draw.text((W//2, sc_y+42), ticket.short_code or 'EVT-????',  font=f_mono,   fill=LAVENDER, anchor="mm")
        draw.text((W//2, sc_y+74), "Type at gate if QR doesn't scan", font=f_mono_s, fill=MUTED,   anchor="mm")

        # ── Status ──
        st_y = sc_y + bh + 22
        if ticket.checked_in:
            draw.rounded_rectangle([(W//2-70, st_y), (W//2+70, st_y+32)], radius=16, fill=(20,60,30), outline=GREEN, width=2)
            draw.text((W//2, st_y+16), "CHECKED IN", font=f_sm, fill=GREEN, anchor="mm")
        else:
            draw.rounded_rectangle([(W//2-50, st_y), (W//2+50, st_y+32)], radius=16, fill=(40,30,80), outline=PURPLE, width=2)
            draw.text((W//2, st_y+16), "VALID", font=f_sm, fill=LAVENDER, anchor="mm")

        # ── Footer ──
        draw.rectangle([(0, H-44), (W, H)], fill=DARK)
        draw.text((36, H-28),   "EventHub · Digital Pass", font=f_xs, fill=MUTED)
        draw.text((W-36, H-28), "eventhub.com",            font=f_xs, fill=MUTED, anchor="ra")

        # ── Serve ──
        buf = io.BytesIO()
        img.save(buf, format='PNG', optimize=True)
        buf.seek(0)
        fname = f"EventHub-Pass-{ticket.short_code or ticket.ticket_id}.png"
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=fname)
    except Exception as e:
        app.logger.error(f"Download pass error: {str(e)}", exc_info=True)
        flash('An error occurred while generating your pass. Please try again.', 'danger')
        return redirect(url_for('my_tickets'))


@app.route('/verify/<token>')
def verify_ticket(token):
    """Public QR scan landing page — shows ticket info."""
    try:
        ticket = Ticket.query.options(
            db.joinedload(Ticket.order).joinedload(Order.user),
            db.joinedload(Ticket.event).joinedload(Event.venue)
        ).filter_by(qr_token=token).first_or_404()
        return render_template('verify_ticket.html', ticket=ticket)
    except Exception as e:
        app.logger.error(f"Verify ticket error: {str(e)}", exc_info=True)
        flash('Invalid or expired ticket.', 'danger')
        return redirect(url_for('index'))


@app.route('/checkin/<token>', methods=['POST'])
@login_required(role="organizer")
def checkin_ticket(token):
    """Organizer marks a ticket as checked-in. Accepts QR token or short code."""
    try:
        from flask import jsonify
        # Try QR token first, then short code - with eager loading
        ticket = Ticket.query.options(
            db.joinedload(Ticket.order).joinedload(Order.user),
            db.joinedload(Ticket.event)
        ).filter_by(qr_token=token).first()
        
        if not ticket:
            ticket = Ticket.query.options(
                db.joinedload(Ticket.order).joinedload(Order.user),
                db.joinedload(Ticket.event)
            ).filter_by(short_code=token.upper()).first()
        
        if not ticket:
            return jsonify({'status': 'error', 'message': 'Invalid code — ticket not found'}), 404
        
        if ticket.checked_in:
            return jsonify({
                'status': 'already',
                'message': f'Already checked in at {ticket.checked_in_at.strftime("%I:%M %p, %b %d")}',
                'name': ticket.order.user.name,
                'event': ticket.event.name,
                'type': ticket.type
            })
        
        ticket.checked_in    = True
        ticket.checked_in_at = datetime.datetime.now()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Check-in successful! ✅',
            'name': ticket.order.user.name,
            'event': ticket.event.name,
            'type': ticket.type,
            'time': ticket.checked_in_at.strftime('%I:%M %p, %b %d')
        })
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Check-in error: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': 'An error occurred during check-in'}), 500


@app.route('/scanner')
@login_required(role="organizer")
def qr_scanner():
    """Organizer QR scanner page."""
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('qr_scanner.html', events=events)


# ── AI Event Planner ──
@app.route('/ai-planner', methods=['GET', 'POST'])
@login_required(role="organizer")
def ai_planner():
    plan = None
    if request.method == 'POST':
        event_type  = request.form.get('event_type', 'conference')
        budget      = float(request.form.get('budget', 50000))
        guests      = int(request.form.get('guests', 100))
        city        = request.form.get('city', 'Delhi')
        duration    = int(request.form.get('duration', 1))

        # Smart template-based plan generation
        venue_budget   = budget * 0.35
        catering       = budget * 0.25
        decor          = budget * 0.15
        entertainment  = budget * 0.12
        marketing      = budget * 0.08
        misc           = budget * 0.05

        venue_suggestions = {
            'wedding':     ['Banquet Hall', 'Garden Resort', 'Heritage Hotel'],
            'conference':  ['Convention Centre', 'Business Hotel', 'Co-working Space'],
            'party':       ['Rooftop Lounge', 'Club Venue', 'Private Villa'],
            'tech fest':   ['Exhibition Hall', 'University Auditorium', 'Tech Park'],
            'concert':     ['Open-air Amphitheatre', 'Indoor Arena', 'Stadium'],
        }.get(event_type, ['Multipurpose Hall', 'Community Centre', 'Hotel Ballroom'])

        timeline = []
        if duration >= 1:
            timeline += [
                {'time': '8:00 AM',  'task': 'Venue setup & decoration'},
                {'time': '9:30 AM',  'task': 'Team briefing & final checks'},
                {'time': '10:00 AM', 'task': 'Guest registration opens'},
                {'time': '11:00 AM', 'task': 'Opening ceremony / Welcome'},
            ]
        if duration >= 1:
            timeline += [
                {'time': '1:00 PM',  'task': 'Lunch / Networking break'},
                {'time': '2:30 PM',  'task': 'Main program / Activities'},
                {'time': '5:00 PM',  'task': 'Closing remarks'},
                {'time': '6:00 PM',  'task': 'Wrap-up & guest departure'},
            ]
        if duration >= 2:
            timeline += [
                {'time': 'Day 2 – 9:00 AM', 'task': 'Day 2 opening'},
                {'time': 'Day 2 – 12:00 PM', 'task': 'Special sessions'},
                {'time': 'Day 2 – 4:00 PM',  'task': 'Award ceremony / Closing'},
            ]

        plan = {
            'event_type':  event_type.title(),
            'budget':      budget,
            'guests':      guests,
            'city':        city,
            'duration':    duration,
            'venues':      venue_suggestions,
            'timeline':    timeline,
            'costs': {
                'Venue & Logistics':  venue_budget,
                'Catering & F&B':     catering,
                'Decor & Setup':      decor,
                'Entertainment':      entertainment,
                'Marketing & Prints': marketing,
                'Miscellaneous':      misc,
            },
            'tips': [
                f'Book venue at least {4 if guests > 200 else 2} months in advance for {guests} guests.',
                f'For {city}, expect 15-20% premium on weekends.',
                'Get 3 vendor quotes before finalising.',
                'Keep 10% of budget as emergency reserve.',
                f'{"Hire a professional MC for large gatherings." if guests > 150 else "A self-hosted MC works well for intimate events."}',
            ]
        }

    return render_template('ai_planner.html', plan=plan)


# ── Reminders ──
@app.route('/reminders')
@login_required(role="attendee")
def reminders():
    try:
        user_id = session['user_id']
        my_reminders = Reminder.query.options(
            db.joinedload(Reminder.event)
        ).filter_by(user_id=user_id).order_by(Reminder.remind_at).all()
        
        # Get events the user has tickets for
        booked_event_ids = db.session.query(Ticket.event_id).join(Order).filter(Order.user_id == user_id).distinct().all()
        booked_events = [Event.query.get(eid[0]) for eid in booked_event_ids if Event.query.get(eid[0])]
        
        return render_template('reminders.html', reminders=my_reminders, events=booked_events)
    except Exception as e:
        app.logger.error(f"Reminders error: {str(e)}", exc_info=True)
        flash('An error occurred while loading reminders.', 'danger')
        return render_template('reminders.html', reminders=[], events=[])

@app.route('/reminders/add', methods=['POST'])
@login_required(role="attendee")
def add_reminder():
    event_id   = request.form.get('event_id', type=int)
    remind_at  = request.form.get('remind_at')
    method     = request.form.get('method', 'email')
    message    = request.form.get('message', '')
    try:
        remind_dt = datetime.datetime.strptime(remind_at, '%Y-%m-%dT%H:%M')
        r = Reminder(user_id=session['user_id'], event_id=event_id,
                     remind_at=remind_dt, method=method, message=message)
        db.session.add(r)
        db.session.commit()
        flash('Reminder set successfully! ✅', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error setting reminder: {e}', 'danger')
    return redirect(url_for('reminders'))

@app.route('/reminders/<int:reminder_id>/delete', methods=['POST'])
@login_required(role="attendee")
def delete_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    if r.user_id != session['user_id']:
        flash('Access denied.', 'danger')
        return redirect(url_for('reminders'))
    db.session.delete(r)
    db.session.commit()
    flash('Reminder deleted.', 'info')
    return redirect(url_for('reminders'))


# ── AI Chat API ──
@app.route('/api/chat', methods=['POST'])
def ai_chat():
    from flask import jsonify
    data = request.get_json()
    msg  = (data.get('message', '') or '').lower().strip()

    # Smart rule-based responses
    responses = {
        ('book', 'ticket', 'how to book'): "To book a ticket: Browse Events → click an event → choose ticket type → click Book Now → select payment method → confirm! 🎟️",
        ('cancel', 'refund'): "You can cancel tickets from My Tickets page. Click Cancel next to any ticket. Refunds are processed within 5-7 business days. 💳",
        ('payment', 'pay', 'upi', 'card', 'paypal'): "We accept Credit/Debit Cards, PayPal, and UPI/Net Banking (GPay, PhonePe, BHIM). All payments are 100% secure. 🔒",
        ('organizer', 'create event', 'host'): "Sign up as an Organizer to create events! Go to Dashboard → Create New Event. You can add venues, speakers, and ticket types. 🎪",
        ('venue', 'location', 'place'): "Venues are managed by organizers. Each event shows its venue details including address, city, and capacity. 📍",
        ('speaker', 'speakers'): "Speakers are added by organizers per event. Check the event details page to see all speakers and their bios. 🎤",
        ('reminder', 'notify', 'alert'): "Set reminders for your booked events from the Reminders page! Choose email or SMS and pick your preferred time. ⏰",
        ('ai planner', 'plan event', 'planning'): "Use our AI Event Planner (organizers only) to get venue suggestions, cost breakdown, and timeline for your event! 🤖",
        ('hello', 'hi', 'hey', 'hii'): "Hey there! 👋 I'm EventHub's AI assistant. Ask me anything about booking tickets, creating events, payments, or planning! 🎉",
        ('help', 'support', 'assist'): "I can help with: booking tickets, cancellations, payments, creating events, venue info, reminders, and event planning! What do you need? 🙋",
        ('price', 'cost', 'fee', 'charge'): "Ticket prices vary by event and type (General, VIP, etc.). Check the event details page for exact pricing. 💰",
        ('thank', 'thanks', 'great', 'awesome'): "You're welcome! Happy to help. Enjoy your event! 🎊",
    }

    reply = None
    for keywords, response in responses.items():
        if any(k in msg for k in keywords):
            reply = response
            break

    if not reply:
        # Generic fallback
        if any(c.isalpha() for c in msg):
            reply = "I'm not sure about that specific query. Try asking about: booking tickets, payments, creating events, venues, speakers, or reminders! 😊"
        else:
            reply = "Please type a message and I'll help you! 😊"

    return jsonify({'reply': reply})


if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        # In production, consider using Flask-Migrate for database migrations
        db.create_all()
    app.run(debug=True) # Set debug=False in production

