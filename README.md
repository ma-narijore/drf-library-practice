# DRF Library Practice
A REST API for a library borrowing service, built with Django REST Framework.
It manages books, users (JWT auth), borrowings, and payments.
## Tech Stack
- Django (`config/settings.py`)
- Django REST Framework
- djangorestframework-simplejwt (JWT auth)
- SQLite (default database)
## Apps
- `books` — book catalog (CRUD; read open to all, writes admin-only)
- `users` — custom email-based user model + registration / JWT endpoints
- `borrowings` — borrow/return books, with inventory tracking
- `payments` — payment records linked to borrowings
## Running Locally
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
The API is available at http://localhost:8000/.

## Running with Docker
```bash
docker build -t drf-library .
docker run -p 8000:8000 drf-library
```
Or with docker-compose:
```bash
docker compose up --build
```

## Creating a Superuser
```bash
python manage.py createsuperuser
```
# in Docker:
```bash
docker compose run --rm web python manage.py createsuperuser
```
## Seeding the Database
`scripts/seed_db.py` requires `django-extensions`:

```bash
python manage.py runscript seed_db
```
## API Endpoints
All routes are prefixed with `/api/v1/`.

**Auth & Users (`users/urls.py`)**
* `POST /api/v1/users/` — register
* `POST /api/v1/users/token/` — obtain JWT pair
* `POST /api/v1/users/token/refresh/` — refresh token
* `GET /api/v1/users/me/`— current user (auth required)

**Books (`books/urls.py`)**
* `GET /api/v1/books/` — list (public)
* `POST /api/v1/books/` — create (admin)
* `GET /api/v1/books/{id}/` — retrieve (public)
* `PUT/PATCH/DELETE /api/v1/books/{id}/`— admin

**Borrowings (`borrowings/urls.py`)**
* `GET /api/v1/borrowings/` — list own (admins see all; filter `?user_id=` and `?is_active=`)
* `POST /api/v1/borrowings/` — create a borrowing (decrements book inventory)
* `GET /api/v1/borrowings/{id}/` — retrieve
Authenticate by sending `Authorization: Bearer <access_token>`.

