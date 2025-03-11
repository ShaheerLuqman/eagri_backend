# EAgri Backend

This is the backend server for the EAgri application, built with Django and PostgreSQL (Neon DB).

## Prerequisites

- Python 3.10 or higher
- PostgreSQL (via Neon DB)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ShaheerLuqman/eagri_backend
cd eagri_backend
```

### 2. Set Up a Virtual Environment

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Place the provided `.env` file in the root directory of the project. This file should contain:

- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Neon DB connection string
- Other environment-specific variables

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

## Running the Server

### Start the Development Server

#### Windows:
```bash
python manage.py runserver
```

#### macOS/Linux:
```bash
python3 manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## Database Information

This project uses Neon DB (PostgreSQL) for the database. The connection is configured using the `DATABASE_URL` environment variable in the `.env` file.

## API Documentation

Once the server is running, you can access the API documentation at:
- http://127.0.0.1:8000/api/docs/ (if available)

## Troubleshooting

If you encounter any issues:

1. Ensure your virtual environment is activated
2. Verify that all environment variables are correctly set
3. Check that the database connection is working properly

