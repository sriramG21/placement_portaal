# Placement Portal Application

A web-based placement management system built with Flask, allowing Admin, Company, and Student roles to interact with campus recruitment activities.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

## Installation

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   python run.py

4. Open browser and visit:
   http://127.0.0.1:5000

## Default Admin Credentials
- Email: admin@gmail.com
- Password: 1234sriram

## Folder Structure
- app/blueprints/ → Route handlers for each role
- app/models.py → Database models
- app/templates/ → HTML templates
- app/static/ → CSS, JS, uploads

## Tech Stack
- Backend: Flask, SQLAlchemy, Flask-Login
- Frontend: Jinja2, Bootstrap 5
- Database: SQLite