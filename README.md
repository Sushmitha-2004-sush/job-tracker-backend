# Job Application Tracker - Backend API

Django REST API for tracking job applications with JWT authentication.

## Features

- User registration and authentication
- CRUD operations for job applications
- Filter by status and search
- Statistics dashboard
- User-specific data isolation

## Tech Stack

- Django 5.x
- Django REST Framework
- MySQL Database
- JWT Authentication
- Python 3.x

## API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/token/` - Login (get access & refresh tokens)
- `POST /api/token/refresh/` - Refresh access token

### Job Applications
- `GET /api/applications/` - List all applications
- `POST /api/applications/` - Create new application
- `GET /api/applications/{id}/` - Get specific application
- `PUT /api/applications/{id}/` - Update application
- `DELETE /api/applications/{id}/` - Delete application
- `GET /api/applications/statistics/` - Get statistics

### Query Parameters
- `?status=applied` - Filter by status
- `?search=Google` - Search company name or job title

## Installation

1. Create virtual environment:
