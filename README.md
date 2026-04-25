# EventHub

> A modern event management platform for organizers and attendees.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-eventhub--s1xx.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://eventhub-s1xx.onrender.com)

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

## Features

**Attendees** — Browse events, book tickets, manage and cancel bookings

**Organizers** — Create and manage events, venues, speakers, and ticket types

**Administrators** — Full access + manage organizers


## Project Structure

```
EventHub/
├── app.py                  # Main application
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── render.yaml             # Render deployment config
├── create_admin_users.py   # Seed admin users
├── migrations/             # Alembic migrations
├── static/                 # CSS, JS
└── templates/              # HTML templates
```

## Local Setup

```bash
# Clone & setup
git clone https://github.com/aryan45sandilya/EventHub.git
cd EventHub
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install & run
pip install -r requirements.txt
flask db upgrade
python create_admin_users.py
flask run
```

Create a `.env` file:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

## Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Administrator | admin@eventhub.com | Admin@123 |
| Organizer 1 | organizer1@eventhub.com | Org1@123 |
| Organizer 2 | organizer2@eventhub.com | Org2@123 |
