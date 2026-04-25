# EventHub

EventHub is a comprehensive event management platform built with Flask that allows organizers to create and manage events while enabling attendees to browse, book tickets, and manage their event participation.

## Features

### For Attendees
- **User Authentication**: Secure signup and login system
- **Event Discovery**: Browse through available events with detailed information
- **Ticket Booking**: Book tickets for events with multiple ticket types
- **Ticket Management**: View and manage your booked tickets
- **Ticket Cancellation**: Cancel tickets with automatic refund processing

### For Organizers
- **Dashboard**: Comprehensive dashboard with event statistics and management tools
- **Event Management**: Create, edit, and delete events
- **Venue Management**: Add and manage venues for events
- **Speaker Management**: Add speakers to events with their details
- **Ticket Management**: Create and manage different ticket types with pricing
- **Order Overview**: View all orders and tickets sold for your events

### For Administrators
- **User Management**: Manage organizers and attendees
- **Full Access**: Access to all organizer and attendee features

## Project Structure

```
EventHub/
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── create_admin_users.py   # Admin user creation script
├── clean_data.py           # Database cleanup utility
├── migrations/             # Database migration files
├── static/                 # Static assets (CSS, JS)
├── templates/              # HTML templates
└── .env                    # Environment variables (local only)
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EventHub.git
   cd EventHub
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows (CMD)
   venv\Scripts\activate.bat

   # Windows (PowerShell)
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   venv\Scripts\activate

   # Unix / MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   ```

   > No database URL needed — SQLite is used by default locally.

5. **Run migrations**
   ```bash
   flask db upgrade
   ```

6. **Create admin and organizer users**
   ```bash
   python create_admin_users.py
   ```

   This creates the following accounts:

   | Role | Email | Password |
   |------|-------|----------|
   | Administrator | admin@eventhub.com | Admin@123 |
   | Organizer 1 | organizer1@eventhub.com | Org1@123 |
   | Organizer 2 | organizer2@eventhub.com | Org2@123 |

7. **Run the application**
   ```bash
   flask run
   ```

   Open your browser at `http://127.0.0.1:5000`

## Deploying to Render

1. Push your code to GitHub

2. Go to [render.com](https://render.com) and create a new **Web Service**

3. Connect your GitHub repository

4. Render will auto-detect `render.yaml` and configure:
   - **Build Command**: `pip install -r requirements.txt && flask db upgrade && python create_admin_users.py`
   - **Start Command**: `gunicorn app:app`

5. Add environment variables in Render dashboard:
   - `SECRET_KEY` — any long random string
   - `FLASK_APP` — `app.py`
   - `FLASK_ENV` — `production`

6. Click **Deploy** — your app will be live!

> **Note**: Render's free tier uses ephemeral storage, so the SQLite database resets on redeploy. For persistent data, use [Render PostgreSQL](https://render.com/docs/databases) or [PlanetScale](https://planetscale.com) and set `DATABASE_URL` accordingly.

## Database Schema

| Table | Description |
|-------|-------------|
| **user** | Stores user info and roles (attendee, organizer, administrator) |
| **event** | Event details — name, description, date, venue |
| **venue** | Venue information |
| **speaker** | Speakers linked to events |
| **tickettype** | Ticket types with pricing and quantity |
| **ticket** | Individual tickets booked by users |
| **order** | Groups tickets purchased in one transaction |
| **payment** | Payment records for orders |

## Development

### Database Migrations
```bash
flask db migrate -m "your message"
flask db upgrade
```

### Clean Database Data
```bash
python clean_data.py
```

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite (local) / PostgreSQL (production)
- **ORM**: SQLAlchemy, Flask-Migrate
- **Frontend**: HTML, CSS, JavaScript
- **Auth**: bcrypt password hashing
- **Server**: Gunicorn (production)
- **Config**: python-dotenv
