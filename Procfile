release: cd backend && python manage.py migrate
web: cd backend && gunicorn backend.wsgi --workers=3 --threads=6
