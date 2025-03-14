# Django Shop App

This is a Django-based e-commerce shop application that provides functionality for managing products, users, orders, and payments.

## Table of contents
- [Features](#features)
- [Installation](#installation)
- [Run with docker](#running-with-docker-compose)
- [Testing](#testing)
- [API documentation](#api-documentation)

## Features

- Product management (CRUD operations)
- User authentication and management
- Shopping cart functionality
- Order processing and payment integration
- API endpoints for frontend integration

## Fixtures
- Create a superuser
```bash
python manage.py createsuperuser
```
- Load fixtures
```bash
python manage.py loaddata my_data.json
```
- Create a new fixture
```bash
python manage.py dumpdata users products payments orders --indent 4 > my_data.json
```
## Installation

### 1. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root and add the necessary environment variables:
```ini
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Add tailwindcss
```bash
npm install tailwindcss @tailwindcss/cli
npx @tailwindcss/cli -i ./static/input.css  -o ./static/output.css --minify
```
Follow the instructions to set up an admin account.

### 5. Run the Development Server
```bash
python manage.py runserver
```
The app will be available at `http://127.0.0.1:8000/`.

## Running with Docker-Compose

### 1. Build and Start the Containers
```bash
docker-compose up --build -d
```
This will start the Django app along with a PostgreSQL database.

### 2. Access the App
The application will be running at `http://localhost:8000/`.

## Testing
To run the tests, execute:
```bash
pytest
```
Or with Docker:
```bash
docker-compose exec web pytest
```

## API Documentation
API documentation is available at:
```
http://127.0.0.1:8000/api/docs/
```
(if Swagger or DRF Browsable API is enabled)