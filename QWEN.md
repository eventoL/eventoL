# EventoL - Project Context

## Project Overview

**EventoL** is an event management software platform initially developed for the [FLISoL](http://flisol.info/) conference. It is a full-stack web application built with:

- **Backend**: Django 4.2 (Python 3.11+) with Django REST Framework
- **Frontend**: React (Node 16.x) with webpack
- **Database**: PostgreSQL with PostGIS (GeoDjango)
- **Async Tasks**: Celery with Redis broker
- **Real-time**: Django Channels (WebSocket support)
- **Authentication**: django-allauth with SAML SSO support

The project supports multi-language translations (8 languages) and follows a Docker-first deployment strategy.

## Repository Structure

```
eventoL/
├── eventol/                    # Main application directory
│   ├── eventol/               # Django project package (settings, urls, celery, api)
│   ├── manager/               # Primary Django app (models, views, forms, tasks, tests)
│   ├── front/                 # React frontend application
│   ├── conf/locale/           # Translation files (8 languages)
│   ├── static/                # Collected static files
│   └── manage.py              # Django management script
├── deploy/                    # Deployment configurations
│   └── docker/                # Docker Compose files and scripts
├── docs/                      # Documentation
├── .github/                   # GitHub configurations (CONTRIBUTING.md, workflows)
├── requirements.txt           # Production Python dependencies
├── requirements-dev.txt       # Development Python dependencies
├── pyproject.toml            # Ruff, isort configuration
├── Makefile                   # Build automation commands
├── Dockerfile                 # Docker image definition
└── .pre-commit-config.yaml    # Pre-commit hooks (ruff linting/formatting)
```

## Building and Running

### Development Setup (Local + Docker Services)

```bash
# 1. Set up Python environment (requires pyenv with Python 3.11+)
pyenv local 3.11.11
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -U pip wheel
pip install -r requirements-dev.txt

# 3. Install pre-commit hooks
pre-commit install

# 4. Start infrastructure services (PostgreSQL/PostGIS, Redis)
cd deploy/docker && docker compose up -d postgres redis

# 5. Configure environment
cp .env.template .env  # Edit as needed

# 6. Run migrations
DJANGO_CONFIGURATION=Dev python eventol/manage.py migrate

# 7. Create superuser
DJANGO_CONFIGURATION=Dev python eventol/manage.py createsuperuser

# 8. Run development server
DJANGO_CONFIGURATION=Dev python eventol/manage.py runserver 0.0.0.0:8000
```

### Full Docker Development Environment

```bash
# Start all services (worker, reactjs, postgres, redis, celery, nginx)
make deploy-dev

# View logs
make logs-follow-dev

# Stop services
make stop-dev
```

### Key Makefile Commands

| Command | Description |
|---------|-------------|
| `make backend-install-dev` | Install Python development dependencies |
| `make backend-test` | Run backend tests with coverage |
| `make backend-migrate` | Run Django migrations |
| `make backend-createsuperuser` | Create admin superuser |
| `make backend-lint` | Run pylint on backend code |
| `make backend-make-translations` | Update translation files (.po) |
| `make backend-compile-translations` | Compile translation files (.mo) |
| `make frontend-install-dependencies` | Install Node.js dependencies (yarn) |
| `make frontend-build` | Build frontend for production |
| `make frontend-build-dev` | Build frontend for development |
| `make frontend-test` | Run frontend tests |
| `make frontend-lint` / `make frontend-lint-fix` | Run ESLint / auto-fix |
| `make deploy-dev` | Deploy full development environment with Docker |
| `make docker-backend-test` | Run tests inside Docker container |

### Docker Compose Services

| Service | Port | Purpose |
|---------|------|---------|
| `worker` | 8000 | Django (Gunicorn in prod, runserver in dev) |
| `reactjs` | 3000 | React development server |
| `postgres` | 5432 | PostGIS database |
| `redis` | 6379 | Cache + Celery broker |
| `celery_worker` | - | Async task processing |
| `nginx` | 80/443 | Reverse proxy (production) |

## Testing

```bash
# Backend tests (pytest-django)
make backend-test
cd eventol && DJANGO_CONFIGURATION=Test python -m pytest manager/tests/test_file.py

# Frontend tests
make frontend-test

# Docker-based testing
make docker-backend-test
```

- **Coverage reports**: HTML at `eventol/htmlcov/`, XML at `eventol/coverage.xml`
- **Test configuration**: `pytest.ini` in project root
- **CI**: GitLab CI (`.gitlab-ci.yml`) with stages: testing → styling → build → deploy

## Development Conventions

### Code Style & Linting

- **Python**: Ruff (linter + formatter) via pre-commit hooks
  - Configuration: `pyproject.toml` (line-length: 120, Python 3.11+)
  - Pre-commit: `.pre-commit-config.yaml` (auto-fix on commit)
  - Manual: `make backend-lint` / `make backend-lint-fix`

- **JavaScript/React**: ESLint + SassLint
  - Commands: `make frontend-lint`, `make frontend-lint-fix`, `make frontend-sasslint`

### Pre-commit Hooks

```bash
# One-time setup
pre-commit install

# Hooks automatically run on commit:
# - ruff --fix (linter with auto-fix)
# - ruff format (code formatter)
```

### Git Workflow

- Branch naming: `<issue-number>-<descriptive-name>` (e.g., `325-add-japanese-translations`)
- Pull requests require:
  - CI passing (tests, linters)
  - Updated with current master
  - No requested changes

### Environment Variables

Copy `.env.template` to `.env` and configure:

- `DJANGO_CONFIGURATION`: Dev, Prod, or Test
- `SECRET_KEY`: Django secret key
- `DEBUG`: Enable debug mode
- `POSTGRES_*`: Database connection settings
- `CELERY_*`: Celery broker configuration
- `EMAIL_*`: Email backend settings

## Key Dependencies

### Backend (Python)

- Django 4.2, djangorestframework 3.15.2
- django-allauth 65.1.0 (authentication)
- django-jazzmin 3.0.1 (admin UI)
- celery 5.x, redis 5.2.1 (async tasks)
- django-channels (WebSocket/ASGI)
- psycopg2-binary (PostgreSQL adapter)
- GDAL (GeoDjango spatial support)
- python3-saml (SAML SSO)

### Frontend (Node.js)

- React with webpack
- Node 16.x required (incompatible with host Node 24 - use Docker)
- yarn package manager

## Important Notes

1. **GeoDjango**: Requires PostGIS and GDAL libraries (provided in Docker image)
2. **setuptools<65**: Required due to django-allauth compatibility
3. **Frontend in Docker**: React development must run in Docker container due to Node version requirements
4. **Translations**: 8 languages supported (en, es, fr, de, nl, no, sv, zh) via Weblate
5. **Static files**: Collected via `make backend-collectstatic` or `make docker-backend-collectstatic`

## Documentation & Resources

- **Official docs**: http://eventol.github.io/eventoL/
- **Contributing guide**: `.github/CONTRIBUTING.md`
- **Development setup**: `develop.md`
- **Migration guide**: `migrate_to_2_to_3.md`
- **Support**: Telegram group https://t.me/eventol_soporte
- **Repositories**: GitHub (main), GitLab (mirror for CI/CD)
