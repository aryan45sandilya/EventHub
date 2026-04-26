# EventHub 🎉

> A comprehensive event management platform built with Flask for seamless event organization and ticket booking.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-eventhub--s1xx.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://eventhub-s1xx.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)](https://eventhub-s1xx.onrender.com)

## ✨ Key Highlights

- 🚀 **Production Ready** - Fully deployed and tested on Render
- 🔒 **Secure** - Bcrypt password hashing, CSRF protection
- 📱 **Responsive** - Mobile-friendly design
- ⚡ **Fast** - Optimized database queries with eager loading
- 🎨 **Modern UI** - Clean and intuitive interface
- 🔧 **Maintainable** - Well-structured codebase with comprehensive error handling

## 🚀 Features

### For Attendees 👥
- 🎫 **Browse Events** - Discover upcoming events with detailed information
- 💳 **Book Tickets** - Multiple payment options (Credit Card, PayPal, UPI)
- 📱 **Digital Pass** - QR code-based tickets with downloadable passes
- 🔔 **Reminders** - Set email/SMS reminders for events
- ✅ **Manage Tickets** - View, download, and cancel tickets easily
- 🎟️ **Ticket Types** - Choose from General, VIP, and other ticket categories

### For Organizers 🎪
- 📅 **Event Management** - Create, edit, and delete events
- 🏢 **Venue Management** - Add and manage event venues
- 🎤 **Speaker Management** - Assign speakers to events
- 🎟️ **Ticket Configuration** - Set ticket types, prices, and quantities
- 📊 **Dashboard** - Real-time analytics and ticket tracking
- ✓ **QR Scanner** - Verify and check-in attendees with QR codes
- 🤖 **AI Event Planner** - Smart event planning with budget breakdown

### For Administrators 🔐
- 👥 **User Management** - Full system access and control
- 🔐 **Organizer Management** - Add, edit, and remove organizers
- 📈 **System Analytics** - System-wide statistics and insights
- 🛡️ **Security** - Monitor and manage platform security

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- Flask 3.0+ (Web Framework)
- SQLAlchemy 2.0+ (ORM with eager loading optimization)
- SQLite (Database)
- Flask-Migrate (Database Migrations)
- Bcrypt (Password Hashing)
- QRCode & Pillow (QR Code Generation)

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive Design
- Modern UI/UX
- Real-time form validation

**Deployment & DevOps:**
- Gunicorn (WSGI Server)
- Render (Cloud Platform)
- Git (Version Control)
- Automated CI/CD Pipeline

**Key Features:**
- ✅ Eager loading for optimized database queries
- ✅ Comprehensive error handling
- ✅ Production logging with rotating file handler
- ✅ Health check endpoint for monitoring
- ✅ Global error handlers (500, 404)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

## 📁 Project Structure

```
EventHub/
├── app.py                      # Main Flask application with all routes
├── config.py                   # Configuration settings (Dev/Prod)
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment configuration
├── create_admin_users.py       # Admin user seeding script
├── clean_data.py               # Database cleanup utility
├── .env                        # Environment variables (local)
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
│
├── migrations/                 # Alembic database migrations
│   ├── versions/
│   │   └── 50b22266f809_initial.py
│   ├── env.py
│   ├── alembic.ini
│   └── script.py.mako
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── script.js          # Main JavaScript
│       └── event-validation.js # Form validation
│
├── templates/                  # Jinja2 HTML templates
│   ├── layout.html            # Base template
│   ├── index.html             # Home page
│   ├── events.html            # Events listing
│   ├── event_details.html     # Event details
│   ├── event_form.html        # Create/Edit event
│   ├── dashboard.html         # Organizer dashboard
│   ├── my_tickets.html        # User tickets
│   ├── digital_pass.html      # QR code pass
│   ├── qr_scanner.html        # QR scanner
│   ├── ai_planner.html        # AI event planner
│   ├── reminders.html         # Event reminders
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   └── ...                    # Other templates
│
├── logs/                       # Application logs (production)
│   └── eventhub.log
│
└── docs/                       # Documentation
    ├── TROUBLESHOOTING.md     # Troubleshooting guide
    ├── DEPLOYMENT_CHECKLIST.md # Deployment steps
    └── FIX_SUMMARY.md         # Recent fixes summary
```

## 🔧 Local Setup

### Prerequisites
- Python 3.8+ (3.11+ recommended)
- pip (Python package manager)
- Git
- Virtual environment (recommended)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/aryan45sandilya/EventHub.git
cd EventHub

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows (PowerShell)
venv\Scripts\activate
# Windows (CMD)
venv\Scripts\activate.bat
# Mac/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create .env file (see Environment Configuration below)

# 6. Initialize database
flask db upgrade

# 7. Create admin users (optional but recommended)
python create_admin_users.py

# 8. Start the development server
flask run
# or
python app.py
```

### Environment Configuration

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration (optional, defaults to SQLite)
DATABASE_URL=sqlite:///eventhub.db

# Python Version (for Render)
PYTHON_VERSION=3.11.0
```

### Access the Application

The application will be available at:
- **Local URL:** `http://localhost:5000`
- **Health Check:** `http://localhost:5000/health`

### Testing

```bash
# Run syntax check
python -m py_compile app.py

# Test database connection
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     print("Database connected!")
```

## 👤 Demo Accounts

After running `create_admin_users.py`, you can login with these accounts:

| Role | Email | Password | Access Level |
|------|-------|----------|--------------|
| 👑 Administrator | admin@eventhub.com | Admin@123 | Full system access |
| 🎪 Organizer 1 | organizer1@eventhub.com | Org1@123 | Event management |
| 🎪 Organizer 2 | organizer2@eventhub.com | Org2@123 | Event management |

**Note:** Change these passwords in production!

## 🌐 Deployment

The application is production-ready and deployed on Render with optimized performance and error handling.


## 📊 Database Schema

### Core Models

**User**
- user_id (PK)
- name, email, password
- user_type (organizer/attendee/administrator)

**Event**
- event_id (PK)
- name, description, date, time
- location_id (FK → Venue)

**Venue**
- venue_id (PK)
- name, address, capacity, city, state, zip_code

**Ticket**
- ticket_id (PK)
- event_id (FK → Event)
- order_id (FK → Order)
- price, type, seat_number
- qr_token, short_code
- checked_in, checked_in_at

**Order**
- order_id (PK)
- user_id (FK → User)
- date, total_price
- payment_id (FK → Payment)

**Payment**
- payment_id (PK)
- order_id (FK → Order)
- payment_method, transaction_id

**Speaker**
- speaker_id (PK)
- name, bio
- event_id (FK → Event)

**TicketType**
- ticket_type_id (PK)
- event_id (FK → Event)
- type, price, quantity

**Reminder**
- reminder_id (PK)
- user_id (FK → User)
- event_id (FK → Event)
- remind_at, method, message, sent




**Made with ❤️ by Aryan Sandilya**

[![GitHub followers](https://img.shields.io/github/followers/aryan45sandilya?style=social)](https://github.com/aryan45sandilya)
[![GitHub stars](https://img.shields.io/github/stars/aryan45sandilya/EventHub?style=social)](https://github.com/aryan45sandilya/EventHub)

</div>
