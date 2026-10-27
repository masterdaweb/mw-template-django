# Django on Master da Web

A Django 6 project with PostgreSQL, uploaded files on Object Storage (django-storages), Gunicorn and its migrations on every deploy.

| Service | What it runs |
| --- | --- |
| `web` | Gunicorn; `python manage.py migrate` runs once per deploy; `collectstatic` runs at build and WhiteNoise serves the admin's CSS |

The database comes as `DATABASE_URL`; the public bucket as `AWS_*`, the names django-storages reads; `DJANGO_SECRET_KEY` was generated for you. `FileField` files go to the bucket and are served from its public address.

The home page sends files and shows each one. For the admin, create a user from the service's Terminal tab: `python manage.py createsuperuser`, then sign in at `/admin`.

## Make it yours

1. In the console, open the project and follow **Your code**: copy this
   template to your GitHub and connect the copy to the project.
2. Change `uploads/views.py` and `uploads/templates/`, then push: every push deploys, with no downtime.

## Run it on your machine

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=true DATABASE_URL=postgresql://app:app@localhost:5432/app
python manage.py migrate && python manage.py runserver
```

## Good to know

- The database is reached through the pooler in transaction mode: `DISABLE_SERVER_SIDE_CURSORS` is already on.

*[Português](README.md)*
