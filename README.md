# MedMaster — Healthcare Management System

## Requirements
- Python 3.11+
- pip

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create admin user (optional)
python manage.py createsuperuser

# 4. Run the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## AI Chatbot (optional)
Set your Gemini API key before running:
```bash
# Linux/Mac
export GEMINI_API_KEY=your_key_here

# Windows CMD
set GEMINI_API_KEY=your_key_here
```
Get a free key at: https://makersuite.google.com/app/apikey

## Notes
- Uses SQLite by default — no database setup needed
- No .env file required — all defaults are hardcoded for local dev
- Static files are served automatically in DEBUG mode
