# NotifyHub - Smart Notification System

A Smart Notification System is django based notification management system that provides multi-channel notification delivery with user preferences, delivery tracking and many other features with  complete API documentation.

## 🚀 Features

- **Multi-Channel Notifications**: Support for In-App, Email, and SMS notifications
- **User Preference Management**: Users can configure their notification preferences with notification configuration
- **Notification Types**: Configurable notification types with custom notification code 
- **Delivery Tracking**: Track notification delivery status and history
- **Global & Targeted Notifications**: Send notifications to all users or specific users
- **Rich Content Support**: CKEditor5 integration for rich text notifications
- **RESTful API**: Complete REST API with authentication
- **Swagger Documentation**: Interactive API documentation
- **Custom User Model**: Extended user model with validation logic 
- **Admin Interface**: Django admin with Jazzmin theme to  make attractive and better

## 🛠️ Tech Stack

- **Backend**: Django 5.2.4, Django REST Framework
- **Database**: PostgreSQL (Production and local),
- **Authentication**: JWT with SimpleJWT
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Rich Text**: CKEditor5
- **Deployment**: Docker, Gunicorn
- **Styling**: Jazzmin Admin Theme

## 📋 Prerequisites

- Python 3.12+
- pip
- PostgreSQL (for production)
- Docker (optional)

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone repo_url
cd NotifyHub
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
$.env.sample as this sample is proivded then used in 
your .env 
```

### 5. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser


```

### 6. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 🐳 Docker Setup

### Build and Run with Docker

```bash
# Build the image
docker build -t notifyhub .

# Run the container
docker run -p 8000:8000 -e DEBUG=True notifyhub


#for the compose run 

Run with: `docker-compose up -d`

## 📖 API Documentation

### Access Points

- **Swagger UI**: `http://localhost:8000/api/swagger/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/`

### Authentication

The API uses JWT authentication. First, obtain tokens:

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/user/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login to get tokens
curl -X POST http://localhost:8000/api/v1/user/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
  "is_staff": true
}
```

### Core API Endpoints

#### 1. Notification Types

```bash
# notification types in the system

curl -X GET http://localhost:8000/api/v1/notification/notification/notifications-type/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  filter:channels,ordering:created_date
```

#### 2. Set User Preferences
```bash
# Create notification preference
curl -X POST http://localhost:8000/api/v1/notification/preferences/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notification_type": 1,
    "channel": "email"
  }'
    "channel": "email"


Getting:GET:api/v1/notification/preferences/
Update:PUT:api/v1/notification/preferences/7/
Delete:api/v1/notification/preferences/7/




```

#### 3. Trigger Notifications

```bash
# Send a notification
curl -X POST http://localhost:8000/api/v1/notification/notification/trigger/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "event": "new_login",
  "data": {
    "user_id": "01d71131-042f-4d2c-bb5f-0ac19e3a353a"
  }


```
This event simulate when user is login and this simulates the notification delivery to user of id 1 with type as mention in perfernces delivery status and only simulate by admin as they are authorize to perform this action

```bash
curl -X POST http://localhost:8000/api/v1/notification/notification/trigger/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "event": "new_comment",
  "data": {
    "comment": "This is sample comment text.",
    "post_id": "123",              
    "author": "UserA",             
    "messages": "Hi.. Mataes"      
  }


```
This event simulate new_comment notification type  and this simulates the notification delivery to alll user of with type who are as mention in perfernces variety of channels and this new_comments type delivery status and only simulate by admin as they are authorize to perform this action

```bash
curl -X POST http://localhost:8000/api/v1/notification/notification/trigger/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "event": "weekly_summary",
  "data": {
    "week_start": "2025-07-01",
    "week_end": "2025-07-07",
    "new_comments": 5,
    "new_logins": 2,
    "summary": "You have 5 new comments and 2 logins this week."
  }
```
This event simulate weekly summary notification type  and this simulates the notification delivery to alll user of with type as mention in perfernces delivery status as weekly_summary with diffrent channels and only simulate by admin as they are authorize to perform this action






#### 4. Get Notification History

```bash

curl -X GET http://localhost:8000/api/v1/notification/history/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
fetch with diffrent filter in query as provided
# Get unread notifications
curl -X GET http://localhost:8000/api/v1/notification/unread/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5. Mark Notifications as Read

```bash
# Mark specific notification as read
curl -X POST http://localhost:8000/api/v1/notification/read/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notification_delivery_id": "delivery-uuid"
  }'
```

### Postman Collection

Import the OpenAPI schema into Postman:
1. Open Postman
2. Click "Import"
3. Enter URL: `http://localhost:8000/api/`
4. Configure authentication with your JWT token

## 📊 API Response Examples

### Successful Notification Trigger Response
```json
{
  "message": "Notification sent successfully",
  "notification_id": "uuid-here",
  "delivery_count": 2,
  "failed_deliveries": []
}
```

### Notification History Response
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "delivery-uuid",
      "notification": {
        "id": "notification-uuid",
        "title": "Welcome Message",
        "content": "Welcome to our platform!",
        "notification_type": {
          "notification_code": "welcome_message",
          "name": "Welcome Message"
        }
      },
      "channel": "email",
      "status": "sent",
      "sent_at": "2025-07-24T10:30:00Z",
      "read_at": null,
      "error_message": null
    }
  ]
}
```

## 🔧 Configuration

### Notification Types Setup

Create notification types via Django admin or API:

```python
# Example notification types
NOTIFICATION_TYPES = [
    {
        "notification_code": "welcome_message",
        "name": "Welcome Message",
        "description": "Sent when a user joins the platform"
    },
    {
        "notification_code": "password_reset",
        "name": "Password Reset",
        "description": "Sent when user requests password reset"
    }
]
```

### Email Configuration

For email notifications, configure your email backend in settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'NotifyHub <noreply@notifyhub.com>'
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test notification
python manage.py test user

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📁 Project Structure

```
NotifyHub/
├── notification/           # Notification app
│   ├── models.py          # Notification models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── signals.py         # Django signals
│   └── urls.py            # URL routing
├── user/                  # User management app
│   ├── models.py          # Custom user model
│   ├── managers.py        # User manager
│   ├── serializers.py     # User serializers
│   └── views.py           # User views
├── utils/                 # Utility modules
│   ├── base_model.py      # Base model classes
│   └── email.py           # Email utilities
├── static/                # Static files
├── staticfiles/           # Collected static files
├── NotifyHub/             # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── manage.py              # Django management script
└── README.md              # This file
```

## 🚀 Deployment

### Production Settings

1. Set `DEBUG=False` in your environment
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving
4. Configure email backend for notifications
5. Set secure `SECRET_KEY`

### Using Docker in Production

```bash
# Build production image
docker build -t notifyhub:latest .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  -e DEBUG=False \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  notifyhub:latest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support

For support and questions, please contact:
- Email: support@notifyhub.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/notifyhub/issues)

## 🔄 Changelog

### v1.0.0 (2025-07-24)
- Initial release
- Multi-channel notification system
- User preference management
- REST API with JWT authentication
- Swagger documentation
- Docker support
