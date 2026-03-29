### INF601 - Advanced Programming in Python
### Zach Slusser
### Mini Project 4


# Weather Updater

A Django web application that lets authenticated users look up current weather conditions by U.S. ZIP code. Every search is saved to the database so all users can see recent lookups, and each user has a personal "My Searches" history page.

## Description

I found the `python-weather` API and wanted to try it out, so I incorporated it into this Django project for my Advanced Python class. The app includes user registration and login powered by Django's built-in authentication system. Once logged in, a user enters a ZIP code and the app fetches live weather data (temperature, humidity, and a text description of current conditions) using the `python-weather` async client. Each lookup is stored in a SQLite database. The home page shows the three most recent searches to unauthenticated visitors, while the main index page (login required) shows the ten most recent searches from all users. A dedicated "My Searches" page lets each user review only their own history.

## Getting Started

### Dependencies

- Python 3.10 or newer (Python 3.12 recommended)
- pip
- All Python package dependencies are listed in `requirements.txt` and installed via pip (see [Installing](#installing) below)
- No external database software is required — the project uses Django's default SQLite backend, which is bundled with Python

### Installing

1. **Clone or download the repository** and open a terminal in the project root (the folder that contains `requirements.txt` and `mysite/`).

2. **Create and activate a virtual environment** *(recommended)*:

   ```bash
   python -m venv venv
   ```

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

### Executing the Program

All `manage.py` commands must be run from inside the `mysite/` directory (where `manage.py` lives).

```bash
cd mysite
```

#### 1. Create the database migration files

This inspects your models and generates the SQL migration files needed to set up the database schema:

```bash
python manage.py makemigrations
```

#### 2. Apply the migrations

This executes the generated SQL and creates all tables in the SQLite database (`db.sqlite3`):

```bash
python manage.py migrate
```

On a brand-new database, this step also seeds 3 starter weather search entries so the public home page has recent results immediately.

#### 3. Create a superuser (admin account)

This creates the administrator account used to access the `/admin` panel. You will be prompted to choose a username, email address, and password:

```bash
python manage.py createsuperuser
```

#### 4. Start the development server

```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**.

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Public home page — shows the 3 most recent searches |
| `http://127.0.0.1:8000/weather/` | Main search page (login required) |
| `http://127.0.0.1:8000/weather/my_searches/` | Personal search history (login required) |
| `http://127.0.0.1:8000/accounts/login/` | Login page |
| `http://127.0.0.1:8000/accounts/signup/` | Registration page |
| `http://127.0.0.1:8000/admin/` | Django admin panel (superuser only) |

## Help

If the weather lookup returns an error, verify that your machine has an active internet connection. The `python-weather` library fetches data from an external service, so network access is required at runtime.

## Authors

Zach Slusser — [@zsluss](https://github.com/zsluss)

## Version History

- **0.1** — Initial release: user auth, ZIP-code weather lookup, shared and personal search history

## License

This project is licensed under the Zach Slusser License — see the LICENSE.md file for details.

## Acknowledgments

- [python-weather](https://github.com/null8626/python-weather) — lightweight async weather client used to fetch live conditions
- [Django](https://www.djangoproject.com/) — web framework powering the backend, authentication, and ORM
