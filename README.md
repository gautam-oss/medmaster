# MedMaster — Healthcare Management System

## Tech Stack
- **Backend**: Django 5.2 · Python 3.11
- **Database**: SQLite (local) · PostgreSQL (Docker + AWS)
- **AI**: Google Gemini API
- **ML**: Linear Regression (insurance cost predictor)
- **Container**: Docker · Docker Compose
- **CI/CD**: GitHub Actions → AWS ECR

---

## Quick Start — Local Dev (WSL)

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install local dependencies
pip install -r requirements/local.txt

# 3. Copy env template and fill in your values
cp .env.example .env.local
# edit .env.local — add your GEMINI_API_KEY if you want the chatbot

# 4. Run migrations
python manage.py migrate

# 5. Create admin user (optional)
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Run with Docker + Postgres

```bash
# 1. Copy production env template and fill in values
cp .env.example .env.production
# edit .env.production — set SECRET_KEY, DB_PASSWORD

# 2. Build and start
docker-compose up --build

# 3. Stop
docker-compose down
```

---

## Run Tests

```bash
pytest tests/ -v
```

---

## Requirements Structure

| File | Used by | Contains |
|------|---------|----------|
| `requirements/base.txt` | everyone | Django, Pillow, numpy, Gemini |
| `requirements/local.txt` | WSL dev | base + pytest + pytest-django |
| `requirements/ci.txt` | GitHub Actions | base + pytest + pytest-django |
| `requirements/production.txt` | Docker / AWS | base + gunicorn + psycopg2 + S3 |

---

## Environment Files

| File | Purpose | Committed? |
|------|---------|------------|
| `.env.example` | template — shows all required keys | ✅ yes |
| `.env.local` | WSL local dev values | ❌ gitignored |
| `.env.production` | Docker + AWS values | ❌ gitignored |

---

## Deployment Phases

- ✅ Phase 1 — Local Django (SQLite)
- ✅ Phase 2 — Docker + Postgres
- ✅ Phase 3 — CI/CD (GitHub Actions → ECR)
- ⏳ Phase 4 — EC2 production server
- ⏳ Phase 5 — RDS + S3 + HTTPS
- ⏳ Phase 6 — CloudWatch monitoring

---

## AI Chatbot Setup

Get a free Gemini API key at: https://makersuite.google.com/app/apikey

Add it to `.env.local`:
```
GEMINI_API_KEY=your-key-here
```