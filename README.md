# Toy Blog Project

### Instruction to start project
- Install Python 3.11 version or higher
- Upgrade pip with new version
- Install pipx
```bash
$ python -m pip install upgrade pip
```
- Install pipx
```bash
$ pip install pipx
```
- After pipx is installed, now install poetry
```bash
$ pipx install poetry
```
- Now run poetry to create virtualenv
```bash
$ poetry shell
```
- Install packages needed for car-repair-shop
```bash
$ poetry install
```
- Run migration script for models
```bash
$ python manage.py migrate
```
- Start Django project and use http://127.0.0.1:8000/
```bash
$ python manage.py runserver
```

### Running local tests and validations
- Before committing run nox validation
```bash
$ nox -s lint tests
```

### Local environment configuration

```bash
# Controls if application is started in debug mode.
# Supported values: True, False
DEBUG=True

# Secret key used in cryptographic functions.
SECRET_KEY="django-insecure-r_!-g^d#6kkf%yxxj0_-8qq0#i6)9*@g4&=w(+0^zo!gk**!5+"

# Comma-separated list of host name values.
ALLOWED_HOSTS=localhost

# Database credentials
DB_NAME=toydb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Docker environment configuration

```bash
# Controls if application is started in debug mode.
# Supported values: True, False
DEBUG=True

# Secret key used in cryptographic functions.
SECRET_KEY="django-insecure-r_!-g^d#6kkf%yxxj0_-8qq0#i6)9*@g4&=w(+0^zo!gk**!5+"

# Comma-separated list of host name values.
ALLOWED_HOSTS=localhost

# Database credentials
DB_NAME=toydb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432
```
### Running docker ssh to create superuser and follow instructions
```bash
$ make ssh
$ python manage.py createsuperuser
```