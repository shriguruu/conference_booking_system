# Conference Booking System

A comprehensive Django-based web application for managing conference bookings, speakers, and attendee registrations. This system provides a complete solution for conference organizers to create events, manage registrations, and handle payments.

## 🚀 Features

### Core Functionality
- **User Management**: Registration, login, and role-based access (attendee, admin, organizer)
- **Conference Management**: Create and manage conferences with detailed information
- **Speaker Management**: Add speakers with expertise and contact information
- **Booking System**: Secure booking process with capacity management
- **Payment Integration**: Track payment status and transaction details
- **Feedback System**: Allow attendees to rate and review conferences
- **Search & Filter**: Advanced search functionality for conferences

### User Features
- **Browse Conferences**: View all available conferences with details
- **Book Conferences**: Secure booking with real-time capacity checking
- **My Bookings**: Track personal booking history and status
- **Cancel Bookings**: Cancel bookings with confirmation
- **Download Receipts**: Generate and download PDF receipts
- **Submit Feedback**: Rate and review attended conferences

### Admin Features
- **Conference Management**: Create, edit, and manage conferences
- **Speaker Management**: Add and manage speaker profiles
- **Booking Oversight**: Monitor all bookings and payment status
- **User Management**: Manage user accounts and roles

## 🛠️ Technology Stack

- **Backend**: Django
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap
- **PDF Generation**: ReportLab
- **Form Handling**: Django Widget Tweaks
- **Authentication**: Django's built-in authentication system

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.8 or higher
- MySQL Server
- pip (Python package installer)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/shriguruu/conference_booking_system
cd conference_booking_system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
1. Create a MySQL database named `conference_db`
2. Update database credentials in `conference_system/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'conference_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
conference-booking-system/
├── booking_app/                 # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Django forms
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Admin interface
│   └── templates/              # HTML templates
│       └── booking_app/
│           ├── base.html       # Base template
│           ├── home.html       # Homepage
│           ├── conferences.html # Conference listing
│           ├── booking_form.html # Booking form
│           └── ...             # Other templates
├── conference_system/          # Django project settings
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── static/                     # Static files
│   └── images/                # Image assets
├── manage.py                   # Django management script
└── README.md                  # This file
```









