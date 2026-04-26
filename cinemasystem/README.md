# Cinema Booking System 🎬

Backend system for booking movies, plays, and concerts with basic JWT authentication.

## Tech Stack
- Django
- mysql for database

## Next Step
- Convert to REST API (DRF)
# 📘 Django REST API Project Setup Guide (Copy Ready)

> 📌 Tip: Use the copy button provided by your editor to copy any section quickly.

---

# 🛠️ 1. Prerequisites

Install the following before starting:

* Python 3.x
* pip
* Git
* MySQL (or PostgreSQL later)

Check versions:

```bash
python3 --version
pip --version
git --version
```

---

# 📁 2. Clone or Initialize Project

### Clone from GitHub

```bash
git clone https://github.com/jabaliamunga/goldcinemaapibasedbookingsystem
cd cinemasystem
```

---

# 🐍 3. Create Virtual Environment

```bash
python3 -m venv my_venv
```

### Activate (Linux / Ubuntu)

```bash
source my_venv/bin/activate
```

---

# 📦 4. Install Dependencies

pip install -r requirements.txt



# 📁 7. Project Structure

```txt
your-repo/
│── cinemasystem/
│── hello/
│── my_venv/
│── manage.py
│── .env
│── .gitignore
│── requirements.txt
```

---

# 🔐 8. Environment Variables (.env)

Create `.env` file:

```bash
touch .env
```

### Example `.env`

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=your_db_name
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```
setup all that info
---

# ⚙️ 9. Load Environment Variables

In `settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
```

---

# 🗄️ 10. Database Configuration (MySQL)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}
```

---

# 🧠 11. Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'api',
]
```

---

# 🔄 12. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# ▶️ 13. Run Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

# 📄 14. Git Ignore

```txt
venv/
__pycache__/
*.pyc
db.sqlite3
.env
```

---

# 📤 15. Push to GitHub

```bash
git add .
git commit -m "Initial Django API setup"
git push origin main
```

---

# 🔥 Final Notes

* Never commit `.env`
* Always use virtual environment
* Keep `requirements.txt` updated
* Prefer PostgreSQL for production systems

---
