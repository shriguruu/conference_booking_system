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

- **Backend**: Django 4.x
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
git clone <repository-url>
cd conference-booking-system
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

## 🗄️ Database Models

### Core Models
- **User**: Extended user model with phone and role fields
- **Conference**: Conference details including topic, date, time, capacity, and price
- **Speaker**: Speaker information with expertise
- **Booking**: User conference bookings with status tracking
- **Payment**: Payment transaction details
- **Feedback**: User feedback and ratings

### Relationships
- Conferences can have multiple speakers
- Users can book multiple conferences
- Each booking can have associated payments
- Users can provide feedback for attended conferences

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=mysql://user:password@localhost:3306/conference_db
```

### Static Files
```bash
python manage.py collectstatic
```

## 🚀 Usage

### For Attendees
1. **Register/Login**: Create an account or login to existing account
2. **Browse Conferences**: View available conferences with search and filter options
3. **Book Conference**: Select a conference and complete the booking process
4. **Manage Bookings**: View, cancel, and download receipts for your bookings
5. **Submit Feedback**: Rate and review conferences you've attended

### For Administrators
1. **Access Admin Panel**: Use the Django admin interface at `/admin/`
2. **Manage Conferences**: Create, edit, and delete conferences
3. **Manage Speakers**: Add and update speaker information
4. **Monitor Bookings**: Track all bookings and payment status
5. **User Management**: Manage user accounts and roles

## 🔒 Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Authentication**: Secure login/logout system
- **Role-based Access**: Different permissions for different user roles
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: Django ORM provides protection

## 📊 Features in Detail

### Conference Management
- Create conferences with topics, descriptions, dates, and times
- Set capacity limits and pricing
- Assign multiple speakers to conferences
- Categorize conferences for better organization

### Booking System
- Real-time capacity checking
- Prevent duplicate bookings
- Booking status tracking (pending, confirmed, cancelled)
- Payment status integration

### Payment Tracking
- Multiple payment methods support
- Transaction ID tracking
- Payment status monitoring
- Receipt generation

### Feedback System
- Star rating system
- Comment submission
- One feedback per user per conference
- Rating aggregation

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL server is running
   - Verify database credentials in settings.py
   - Check if database exists

2. **Migration Errors**
   - Delete migration files and recreate them
   - Ensure database is properly configured

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check static files configuration

4. **PDF Generation Issues**
   - Ensure ReportLab is properly installed
   - Check file permissions for PDF generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap for UI components
- ReportLab for PDF generation
- MySQL for database management

## 📞 Support

For support and questions, please contact:
- Email: your-email@example.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/conference-booking-system/issues)

---

**Note**: This is a development version. For production deployment, ensure to:
- Set `DEBUG = False`
- Use environment variables for sensitive data
- Configure proper database settings
- Set up HTTPS
- Implement proper backup strategies 