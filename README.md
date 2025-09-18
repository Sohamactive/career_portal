# Career Portal

A comprehensive Django-based web application for managing internship opportunities and applications. This platform connects students with organizations offering internships, providing a streamlined application process and management system.

## Features

### For Students
- **User Registration & Authentication**: Custom user model with email-based authentication
- **Profile Management**: Complete profile setup with resume and certificate uploads
- **Internship Discovery**: Browse and search available internships
- **Application System**: Apply for internships with Statement of Purpose (SOP) and resume
- **Application Tracking**: Monitor application status and history
- **Dashboard**: Personalized dashboard to manage applications and profile

### For Administrators
- **Admin Panel**: Django admin interface with Jazzmin styling
- **Internship Management**: Create and manage internship listings
- **Application Review**: Review and update application statuses
- **User Management**: Manage user accounts and profiles
- **Analytics**: Track applications and internship statistics

### Application Statuses
- Applied
- Offered
- Accepted
- Working
- Rejected
- Offer Expired
- Auto Rejected
- Declined

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Frontend**: Django Templates with custom CSS
- **Styling**: Tailwind CSS integration
- **Admin Interface**: Django Jazzmin
- **File Handling**: Django's built-in file upload system
- **Authentication**: Custom user model with Django's authentication system

## Project Structure

```
career_portal/
├── career_portal/          # Main project directory
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── applications/          # Application management app
│   ├── models.py          # Application model
│   ├── views.py           # Application views
│   ├── forms.py           # Application forms
│   └── urls.py            # Application URLs
├── internships/           # Internship management app
│   ├── models.py          # Internship and Skill models
│   ├── views.py           # Internship views
│   └── urls.py            # Internship URLs
├── users/                 # User management app
│   ├── models.py          # Custom user model
│   ├── views.py           # User views
│   ├── forms.py           # User forms
│   └── urls.py            # User URLs
├── core/                  # Core app (homepage, etc.)
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
│   ├── resumes/           # Resume uploads
│   ├── certificates/      # Certificate uploads
│   └── profile_pics/      # Profile pictures
└── manage.py              # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd career_portal
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Step 6: Database Setup
```bash
cd career_portal
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### For Students
1. **Register**: Create an account using your email
2. **Complete Profile**: Add personal information, upload resume and certificates
3. **Browse Internships**: View available internship opportunities
4. **Apply**: Submit applications with SOP and resume
5. **Track Progress**: Monitor application status through your dashboard

### For Administrators
1. **Access Admin Panel**: Go to `/admin/` and login with superuser credentials
2. **Add Internships**: Create new internship listings with requirements and details
3. **Manage Applications**: Review and update application statuses
4. **User Management**: Handle user accounts and profile information

## Key Models

### User Model
- Custom user model extending Django's AbstractBaseUser
- Email-based authentication
- Profile fields for academic and personal information
- File uploads for resumes, certificates, and profile pictures

### Internship Model
- Title, description, and requirements
- Paid/Unpaid classification
- Skills required (many-to-many relationship)
- Application deadline and duration
- Position limits and tracking

### Application Model
- Links users to internships
- Tracks application status workflow
- Stores SOP and resume
- Timestamped for tracking

## Configuration

### Database
The project uses SQLite by default. To use PostgreSQL or MySQL, update the `DATABASES` setting in `settings.py`.

### File Uploads
Media files are stored in the `media/` directory with organized subdirectories for different file types.

### Static Files
CSS and other static assets are stored in the `static/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if available)
5. Submit a pull request

## Security Considerations

- Environment variables for sensitive settings
- CSRF protection enabled
- File upload validation
- User authentication required for sensitive operations

## Future Enhancements

- Email notifications for application status changes
- Advanced search and filtering
- Company/organization profiles
- Bulk application management
- API endpoints for mobile app integration
- Advanced reporting and analytics

## Support

For issues and questions, please create an issue in the repository or contact the development team.

