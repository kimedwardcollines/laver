# Laver Transformation Ministries - Django CMS

A fully dynamic, database-driven Content Management System for church websites built with Django.

## Features

### Content Management
- ✅ Church Information (name, logo, mission, vision, history, contact info)
- ✅ Leadership Team (photos, bios, positions)
- ✅ Ministries (with leaders and descriptions)
- ✅ Service Times (weekly schedule)
- ✅ Events (with registration links)
- ✅ Sermons (video, audio, notes)
- ✅ Photo Gallery (albums support)
- ✅ Testimonials (approval workflow)
- ✅ Announcements (with expiry dates)
- ✅ Prayer Requests (status tracking)
- ✅ Newsletter Subscribers
- ✅ Online Giving Information
- ✅ Contact Messages

### Dashboard Features
- 📊 Statistics Dashboard
- 📝 CRUD operations for all content
- 🔔 Notifications (pending items)
- ⚡ Quick Actions
- 📱 Responsive Design

### Technical
- 🛡️ User Authentication
- 📁 Image/File Uploads
- 📱 Bootstrap 5 Responsive Design
- 🎨 Modern UI
- 🔍 Django Admin Integration
- 📄 Rich Text Editing (CKEditor)
- 📧 Email Notifications (configurable)

## Installation

### 1. Create Virtual Environment
```bash
cd django_cms
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Environment File
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Migrations
```bash
python manage.py makemigrations church
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

### 7. Access
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin/
- Dashboard: http://localhost:8000/dashboard/

## Project Structure

```
django_cms/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── laver_website/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── church/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py          # All database models
│   ├── admin.py           # Django Admin configuration
│   ├── views.py           # Public views
│   ├── forms.py           # Form classes
│   ├── urls.py            # Public URL routing
│   ├── dashboard_urls.py   # Dashboard URL routing
│   ├── dashboard_views.py # Dashboard views
│   ├── context_processors.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── dashboard/
│   │   ├── index.html
│   │   └── login.html
│   └── church/
│       ├── home.html
│       └── includes/
│           ├── navbar.html
│           └── footer.html
└── media/                  # Uploaded files (create this directory)
```

## User Roles

### Super Admin
- Full access to all features
- Django Admin access

### Pastor
- Sermons management
- Events management
- Announcements

### Content Editor
- Gallery management
- Testimonials
- Ministries

### Church Staff
- Prayer requests
- Newsletter subscribers

## Environment Variables

Create a `.env` file:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn laver_website.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "laver_website.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Using Render.com
See render.yaml for deployment configuration.

## SEO Features

- Meta descriptions
- Open Graph tags
- Sitemap (sitemap.xml)
- Robots.txt
- Canonical URLs

## License

This project is proprietary for Laver Transformation Ministries.

---

Built with ❤️ for churches everywhere
