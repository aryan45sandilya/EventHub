# EventHub

> A comprehensive event management platform built with Flask for seamless event organization and ticket booking.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-eventhub--s1xx.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://eventhub-s1xx.onrender.com)

## 🚀 Features

### For Attendees
- 🎫 Browse and discover upcoming events
- 💳 Book tickets with multiple payment options
- 📱 Digital tickets with QR codes
- 🔔 Event reminders and notifications
- ✅ Easy ticket management and cancellation

### For Organizers
- 📅 Create and manage events
- 🏢 Venue management
- 🎤 Speaker management
- 🎟️ Ticket type configuration
- 📊 Event analytics and ticket tracking
- ✓ QR code ticket verification

### For Administrators
- 👥 Full system access
- 🔐 Manage organizers and users
- 📈 System-wide analytics

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- Flask-Migrate (Database Migrations)
- Bcrypt (Password Hashing)

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive Design
- QR Code Generation

**Deployment:**
- Gunicorn (WSGI Server)
- Render (Cloud Platform)

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
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── create_admin_users.py       # Admin user seeding script
├── migrations/                 # Alembic database migrations
│   ├── versions/
│   └── env.py
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── script.js          # Main JavaScript
│       └── event-validation.js
└── templates/                  # Jinja2 HTML templates
    ├── layout.html
    ├── index.html
    ├── events.html
    ├── event_details.html
    ├── dashboard.html
    └── ...
```

## 🔧 Local Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/aryan45sandilya/EventHub.git
cd EventHub

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Create admin users
python create_admin_users.py

# Start the development server
flask run
```

### Environment Configuration

Create a `.env` file in the root directory:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///eventhub.db
```

The application will be available at `http://localhost:5000`

## 👤 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Administrator | admin@eventhub.com | Admin@123 |
| Organizer 1 | organizer1@eventhub.com | Org1@123 |
| Organizer 2 | organizer2@eventhub.com | Org2@123 |

## 🌐 Deployment

The application is configured for deployment on Render with SQLite database and persistent storage.

### Deploy to Render

#### Option 1: Using render.yaml (Recommended)

1. Fork this repository to your GitHub account
2. Sign up/Login to [Render](https://render.com)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and configure everything
6. Click "Apply" to deploy

The `render.yaml` includes:
- Automatic dependency installation
- Database migrations
- Admin user creation
- Persistent disk for SQLite database (1GB)
- Environment variables configuration

#### Option 2: Manual Setup

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - **Name:** eventhub
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt && flask db upgrade && python create_admin_users.py`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
4. Add environment variables:
   - `FLASK_APP=app.py`
   - `FLASK_ENV=production`
   - `SECRET_KEY` (auto-generate)
5. Add a persistent disk:
   - **Name:** eventhub-data
   - **Mount Path:** /opt/render/project/src
   - **Size:** 1 GB
6. Deploy!

### Important Notes for Production

- **Database:** SQLite with persistent disk storage on Render
- **Migrations:** Automatically run during deployment
- **Admin Users:** Created automatically via `create_admin_users.py`
- **Static Files:** Served by Flask (for small-scale apps)
- **Security:** SECRET_KEY is auto-generated by Render

### Environment Variables

Required environment variables for production:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=<auto-generated-by-render>
```

### Database Persistence

The SQLite database is stored on a persistent disk mounted at `/opt/render/project/src`. This ensures your data persists across deployments and restarts.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Aryan Sandilya - [@aryan45sandilya](https://github.com/aryan45sandilya)

Project Link: [https://github.com/aryan45sandilya/EventHub](https://github.com/aryan45sandilya/EventHub)
