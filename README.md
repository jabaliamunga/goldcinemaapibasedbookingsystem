# 🎬 Gold Cinema Booking System

A full-stack cinema booking web application built with **Django REST Framework** and **JWT Authentication**. Customers can register, log in, browse productions, check seat availability, and book seats online.

---

## 📸 Features

- 🔐 JWT-based authentication (email + password)
- 🎟️ Book seats for Movies, Plays, and Concerts
- 💺 Real-time seat availability map (300 seats)
- 📧 Automatic email notifications to all customers when a new production is added
- 🛡️ Protected API endpoints
- 🖥️ Full frontend with Tailwind CSS

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0, Django REST Framework |
| Authentication | SimpleJWT |
| Database | MySQL |
| Frontend | HTML, Tailwind CSS |
| Email | Gmail SMTP |
| Language | Python 3.12 |

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/jabaliamunga/goldcinema.git
cd goldcinema
```

### 2. Create and activate virtual environment

```bash
python -m venv my_venv
source my_venv/bin/activate  # Windows: my_venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the root directory

```env
SECRET_KEY=your_django_secret_key

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=Gold Cinema <your@gmail.com>
```

### 5. Create the MySQL database

```sql
CREATE DATABASE your_db_name;
```

### CONFIGURE DATABASE
import os
from dotenv import load_dotenv

load_dotenv()


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

### INSTALLED APPS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'hello',         
]

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```
goldcinema/
├── cinemasystem/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hello/                  # Main app
│   ├── models.py           # Customer, Production, Booking
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API + consumer views
│   ├── urls.py             # URL routes
│   ├── signals.py          # Email on new production
│   ├── admin.py            # Admin config
│   └── templates/
│       ├── index.html      # Landing + login + register
│       ├── account.html    # Booking page
│       └── test.html       ## Seat map page
|       |__ email.html        
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🌐 Pages

| URL | Description | Auth Required |
|---|---|---|
| `/` | Landing page, login, register | No |
| `/productions_page/` | Browse productions + book seats | Yes |
| `/test/` | Check seat availability | Yes |
| `/board/` | Seat map (POST from /test/) | Yes |
| `/admin/` | Django admin panel | Superuser |

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/register_customer/` | Register new customer | No |
| GET | `/api/register_customer/` | Get all customers | No |
| POST | `/api/token/` | Login — get JWT tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |
| GET | `/api/fetch_productions/` | Get all productions | No |
| POST | `/api/booking/` | Book a seat | Yes |
| POST | `/api/fetch_seats/` | Get booked seats for a production | Yes |

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for full request/response examples.

---

## 💰 Pricing

| Production Type | Price (KES) |
|---|---|
| 🎬 Movie | 300 |
| 🎭 Play | 400 |
| 🎵 Concert | 600 |

Prices are automatically applied during booking. Seats are numbered **1 to 300**.

---

## 👤 User Roles

### Customer
- Register and log in
- Browse productions
- Book seats
- Check seat availability

### Admin (Superuser)
- Manage productions (add, edit, delete)
- View all bookings and customers
- Adding a production automatically emails all registered customers

---

## 📧 Email Notifications

When a new production is added via the admin panel, all registered customers automatically receive an email notification with the production name, type, and show date.

Configure Gmail SMTP in `.env`:
```env
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

> ⚠️ Use a **Gmail App Password**, not your regular Gmail password. Enable 2FA on your Google account first, then generate an app password at myaccount.google.com/apppasswords.

---

## 🔐 Authentication Flow

```
Register (/api/register_customer/)
       ↓
Login (/api/token/) → returns access + refresh tokens
       ↓
Use access token in Authorization header
       ↓
Token expires → refresh via (/api/token/refresh/)
```

---

## 🚀 Deployment Notes

- Set `DEBUG = False` in production
- Add your domain to `ALLOWED_HOSTS`
- Use a production WSGI server (e.g. Gunicorn + Nginx)
- Use environment variables for all secrets — never hardcode credentials

---

## 📄 License

This project is for educational purposes.

---

*Built with ❤️ in Nairobi, Kenya — Gold Cinema © 2026*