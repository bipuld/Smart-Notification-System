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
- **Deployment**: Docker, Gunicorn,Render
- **Styling**: Jazzmin Admin Theme

## 📋 Prerequisites

- Python 3.12+
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

The production link:
https://smart-notification-system-nxi5.onrender.com/api/swagger/
For admin :
https://smart-notification-system-nxi5.onrender.com/admin/


## 🐳 Docker Setup

### Build and Run with Docker

```bash
# Build the image
docker build -t notifyhub .

# Run the container
docker run -p 8000:8000 -e DEBUG=True notifyhub


#for the compose run 

Run with: `docker-compose up -d`

```

## 📄 Design Decisions

### 1. Signals for Notification Triggers
Django signals (`post_save`, etc.) were used to decouple event logic from core functionality. For example, triggering notifications on events like user login or comment creation is handled via thorugh notification preference and its deliver to user, making the codebase more modular, reusable, and easier to maintain.

**Benefit**: Promotes loose coupling between business logic and notification system.

### 2. Initialization for Notification Types
Notification types (e.g., `new_login`, `weekly_summary`, `new_comment`) are initialized via custom Django data migrations instead of manual admin entry or seed scripts.

**Benefit**: Ensures consistent and repeatable setup across environments (development, staging, production) without requiring manual configuration.


### 3. Separated Models for Notification Types, Preferences, and Deliveries
The system uses distinct models for:
- `NotificationType`: Defines what kinds of events can trigger notifications.
- `NotificationPreference`: Stores user-level preferences for each notification type and channel.
- `NotificationDelivery`: Tracks each actual delivery attempt (status, channel, timestamp).

**Benefit**: Improves scalability, simplifies querying, and cleanly supports multi-channel delivery logic.


### 4. Custom User Model
A custom user model was used to ensure flexibility for future enhancements such as email login, or user profiles.

**Benefit**: Future-proofs the system while aligning with more features.


### 5. Mock Email and SMS Channels
Since the system uses mocked services for these channels . Delivery logs still track them as if they were real.

**Benefit**: Keeps local setup simple while simulating real-world flows.

### 6. Role-Based Access and Permissions
Sensitive actions like triggering system wide events are protected via permission checks to ensure only admin users can perform them.

**Benefit**: Security and integrity in notification handling.


### 7. DRF-Spectacular for API Documentation
`drf-spectacular` was chosen for its tight integration with Django REST Framework and automatic schema generation. It supports both Swagger and ReDoc UIs.

**Benefit**: Provides clear, interactive API docs for developers and testers.



### 8. CKEditor5 for Rich Text Notifications
Rich content notifications (especially for email) benefit from formatted text. CKEditor5 was integrated for creating and managing content-rich messages in admin.

**Benefit**: Allows admin to create visually appealing notifications with formatting and media.


### 9. Jazzmin for Admin Customization
The default Django admin is enhanced using the **Jazzmin** theme to provide a modern, clean, and user friendly interface. This makes managing users, notification types, preferences, and delivery logs more intuitive for admin users.

**Benefit**: Improves usability and aesthetics of the admin panel without requiring a custom frontend. Helps non-technical admins navigate and manage the system efficiently.

```


## 🐛 Debug Logging

The project includes Django's built-in logging configuration, enhanced with custom debug-level logs to help developers monitor and troubleshoot the notification system. Logging is used to:

- Track when and how notification events are triggered
- Log delivery attempts across channels (in-app, email, SMS)
- Report failures and reasons during notification dispatch
- Capture key user actions (e.g., login, comment creation) when tied to events

```

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
#### 6. List of Delivery Notification 

```bash
# Mark Deleivery Notification 
curl -X POST http://localhost:8000/api/v1/notification/notification-delivery/ 
```

#### 7. List of  Notification Type in the System

```bash
# give all intial notification type
curl -X POST http://localhost:8000/api/v1/notification/notifications-type/


```

### Postman Collection

Import the OpenAPI schema into Postman:
1. Open Postman
2. Click "Import"
3. Enter URL: `http://localhost:8000/api/`
4. Configure authentication with your JWT token


## 🔧 Configuration

### Notification Types Setup

Create notification types via Django admin or default migrations three type is define as : new_login,weekly_summary,new_comment:


### Email Configuration

For email notifications, configure your email backend in settings:

# TODO
```



```


## 🚀 Deployment

### Production Settings

1. Set `DEBUG=False` in your environment
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving
4.Setup allowedhost
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

## 🔄 Changelog

### v1.0.0 (2025-07-24)
- Initial release
- Multi-channel notification system
- User preference management
- REST API with JWT authentication
- Swagger documentation
- Docker support
