# 🚀 PythonAnywhere Deployment Guide

## Step 1: Create Account (2 minutes)

1. Go to: https://www.pythonanywhere.com
2. Click **"Start running Python online in less than a minute!"**
3. **Sign up** (free account)
4. Verify email

---

## Step 2: Open Bash Console (1 minute)

1. Dashboard → **"Consoles"** tab
2. Click **"Bash"** (under "Start a new console")
3. Black terminal khulega

---

## Step 3: Clone Repository (2 minutes)

Bash console mein type karo:

```bash
# Clone your repo
git clone https://github.com/aryan45sandilya/EventHub.git

# Go to directory
cd EventHub

# Check files
ls
```

---

## Step 4: Create Virtual Environment (2 minutes)

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 5: Setup Database (2 minutes)

```bash
# Initialize database
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("Database created!")
EOF

# Create admin users
python create_admin_users.py

# Initialize sample data
python init_production_db.py
```

---

## Step 6: Configure Web App (3 minutes)

1. Dashboard → **"Web"** tab
2. Click **"Add a new web app"**
3. Click **"Next"** (free domain)
4. Select **"Manual configuration"**
5. Select **"Python 3.10"**
6. Click **"Next"**

---

## Step 7: Configure WSGI File (3 minutes)

1. Web tab par scroll down
2. **"WSGI configuration file"** link click karo
3. **Sab delete karo** aur ye paste karo:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/EventHub'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secret-key-change-this'

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Flask app
from app import app as application
```

**Important:** Replace `YOUR_USERNAME` with your PythonAnywhere username!

4. Click **"Save"** (top right)

---

## Step 8: Configure Virtual Environment (1 minute)

1. Web tab par wapas jao
2. **"Virtualenv"** section mein:
   ```
   /home/YOUR_USERNAME/EventHub/venv
   ```
3. Click checkmark to save

---

## Step 9: Configure Static Files (1 minute)

1. **"Static files"** section mein
2. Add:
   ```
   URL: /static/
   Directory: /home/YOUR_USERNAME/EventHub/static
   ```

---

## Step 10: Reload & Test (1 minute)

1. Top par **"Reload"** button (green) - click karo
2. Wait 10 seconds
3. Click your app URL: `https://YOUR_USERNAME.pythonanywhere.com`

---

## ✅ Success!

Dashboard kholo:
```
https://YOUR_USERNAME.pythonanywhere.com/dashboard
```

**Login:**
- Email: `admin@eventhub.com`
- Password: `Admin@123`

---

## 🎉 Done!

✅ 3 Venues dikhenge
✅ 1 Event dikhega
✅ Events create kar sakte ho
✅ Sab kaam karega!

---

## Troubleshooting

### Error: "Something went wrong"
1. Web tab → **"Error log"** click karo
2. Error dekho
3. Fix karo aur **"Reload"** karo

### Database Empty
Bash console mein:
```bash
cd EventHub
source venv/bin/activate
python init_production_db.py
```

### Update Code
```bash
cd EventHub
git pull origin main
# Web tab → Reload button
```

---

## Summary

**Total Time:** 15-20 minutes
**Cost:** FREE
**Result:** Fully working EventHub! 🚀

---

**PythonAnywhere Flask + SQLite ke liye PERFECT hai!**
