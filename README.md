# Booking System

## Overview

todo

## Installation

To run the booking system, you'll need Python 3 and Django. 

Create new Python env

```bash
python -m venv env
```

Activate env

Linux
```bash
source env/bin/activate
```

Windows
```ps1
.\env\Scripts\Activate.ps1
```

Install Requirements

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Rename ```sample.env``` to ```.env```

Make migrations and then run migrations
```
python manage.py makemigrations
python manage.py migrate
```

Create a superuser
```
python manage.py createsuperuser
```

Run server
```
python manage.py runserver
```

Open website
```
http://127.0.0.1:8000/
```