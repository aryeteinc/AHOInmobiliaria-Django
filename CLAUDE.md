# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AHO Inmobiliaria Backend is a Django-based real estate management system for managing properties, advisors, and related data. The project uses Python 3.10+ with Django 5.2+ and MySQL as the primary database.

## Development Commands

### Environment Setup
```bash
# Install dependencies using Poetry
poetry install

# Or using pip with requirements.txt
pip install -r requirements.txt

# Set up environment variables (create .env file based on settings.py)
# Required variables: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, MEDIA_URL, MEDIA_ROOT
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run with specific port
python manage.py runserver 8080
```

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Load initial data (if fixtures exist)
python manage.py loaddata <fixture_name>
```

### Code Quality
```bash
# Format code with Black
black .

# Run Django's built-in checks
python manage.py check
```

### Testing
```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test inmobiliaria

# Run with verbose output
python manage.py test --verbosity=2
```

## Architecture Overview

### Project Structure
- `core/` - Django project configuration and main settings
- `inmobiliaria/` - Main application containing business logic
- `media/` - User-uploaded files (images, documents)

### Key Models (inmobiliaria/models.py)

**Managed Models (Django ORM handles these):**
- `Assesor` - Real estate advisors with photo upload functionality
- `City` - Cities with department information

**Unmanaged Models (Database-first approach):**
- `Inmuebles` - Main property model with extensive property details
- `Barrios` - Neighborhoods linked to cities
- `Caracteristica` - Property characteristics (texto/numerico types)
- `TiposInmueble`, `UsosInmueble`, `EstadosInmueble` - Property classifications
- `Imagenes` - Property images with URL management
- `Etiquetas` - Property tags with color coding

### Database Configuration
- Uses MySQL with PyMySQL adapter
- Configured for environment-based settings via .env file
- Media files stored locally in `media/` directory
- Both managed and unmanaged models coexist (legacy database integration)

### Admin Interface
- Custom admin configurations in `inmobiliaria/admin.py`
- Enhanced display for Assesor model with image previews and formatted phone numbers
- Search, filtering, and pagination configured for all registered models
- Fieldsets organize form fields logically

### URL Configuration
- Main URLs in `core/urls.py`
- Only admin interface currently configured
- Media files served during development

## Development Notes

### Model Relationships
- Mixed approach: some models managed by Django, others unmanaged (existing database)
- Foreign key relationships span both managed and unmanaged models
- `Inmuebles` is the central model with relationships to most other entities

### Image Handling
- `Assesor` model uses ImageField with upload_to='asesores/'
- Media files configuration in settings supports local file storage
- Admin interface provides image previews

### Database Migration Strategy
- Only managed models (Assesor, City) generate migrations
- Unmanaged models rely on existing database schema
- Use `managed = False` in Meta class for database-first models

### Admin Customization
- Extensive admin customization with custom display methods
- Image previews, formatted phone numbers, and status indicators
- Fieldsets group related fields for better UX