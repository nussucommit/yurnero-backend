# yurnero-backend
Backend for the new NUSSU commIT website.

## Quick Start
- set new env (if not done yet) using `venv` or `virtualenv`
- activate env `source {env folder}/bin/activate`
- install dependencies (if not done yet) using `pip install -r requirements.txt`
- start server: `python backend/manage.py runserver`

## Note
- to test API endpoints: remember to place env first.
- create superuser (for admin stuff locally): `python backend/manage.py createsuperuser`
- migrate: `python backend/manage.py migrate`
- make migrations: `python backend/manage.py makemigrations`
