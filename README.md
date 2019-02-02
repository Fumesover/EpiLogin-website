# Epilogin website

This is epilogin website sources. It uses the django python framework along
with html, css and javascript.

# The project

## Development

You will need python3 and pip installed.

First, create a python environment:
> python -m venv .venv
> source venv/bin/activate

Then, install requirements:
> pip3 install -r requirements.txt

Create your local settings. Do not forget to fix the discord credentials
> cp config/local_settings.py.sample config/local_settings.py
> $EDITOR config/local_settings.py

Migrate the database
> python3 manage.py migrate

Load fixtures
> python3 manage.py loaddata config/fixtures/\*

Run the development server on 127.0.0.1:8000
> python3 manane.py runserver



> https://apps.dev.microsoft.com
