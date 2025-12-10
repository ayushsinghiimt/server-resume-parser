# Resume Parser REST API

Django REST Framework backend for the Resume Parser application.

## Features

- 🚀 RESTful API endpoints for resume management
- 📄 Resume file upload and storage
- 👤 Candidate profile management
- 💼 Experience and education tracking
- 🔍 Status-based filtering
- 🌐 CORS enabled for frontend integration
- 📊 Django admin panel for data management

## Tech Stack

- **Django 5.0** - Web framework
- **Django REST Framework** - REST API toolkit
- **SQLite** - Database (development)
- **django-cors-headers** - CORS support

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and update values as needed
```

### 4. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Resumes

- `GET /api/resumes/` - List all resumes
- `POST /api/resumes/` - Create a new resume (supports file upload)
- `GET /api/resumes/{id}/` - Get a specific resume
- `PUT /api/resumes/{id}/` - Update a resume
- `PATCH /api/resumes/{id}/` - Partial update a resume
- `DELETE /api/resumes/{id}/` - Delete a resume
- `GET /api/resumes/by_status/?status=pending` - Filter resumes by status
- `POST /api/resumes/{id}/update_status/` - Update resume status

### Experiences

- `GET /api/experiences/` - List all experiences
- `POST /api/experiences/` - Create a new experience
- `GET /api/experiences/{id}/` - Get a specific experience
- `PUT /api/experiences/{id}/` - Update an experience
- `DELETE /api/experiences/{id}/` - Delete an experience

### Education

- `GET /api/education/` - List all education entries
- `POST /api/education/` - Create a new education entry
- `GET /api/education/{id}/` - Get a specific education entry
- `PUT /api/education/{id}/` - Update an education entry
- `DELETE /api/education/{id}/` - Delete an education entry

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` using the superuser credentials you created.

## Project Structure

```
server-resume-parser/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── resume_parser_project/      # Main Django project
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
└── api/                        # API Django app
    ├── models.py               # Database models
    ├── serializers.py          # DRF serializers
    ├── views.py                # API views/viewsets
    ├── urls.py                 # API URL routing
    └── admin.py                # Admin configuration
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating New Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Shell

```bash
python manage.py shell
```

## Frontend Integration

The API is configured to accept requests from `http://localhost:3000` (your React frontend). To change this, update the `CORS_ALLOWED_ORIGINS` in your `.env` file.

Example fetch from frontend:

```javascript
// Get all resumes
const response = await fetch('http://localhost:8000/api/resumes/');
const resumes = await response.json();

// Create a new resume
const formData = new FormData();
formData.append('full_name', 'John Doe');
formData.append('email', 'john@example.com');
formData.append('resume_file', file);

const response = await fetch('http://localhost:8000/api/resumes/', {
  method: 'POST',
  body: formData,
});
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

## License

MIT
