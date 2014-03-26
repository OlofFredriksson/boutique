# Boutique

Small e-commerce solution implemented in Django for educational purposes.

The code here might not be optimal, or even correct. It is only intended to
show off Django features and the best practise to setup a Django project.

This file contains what is needed to setup the project and run the server.

Some understanding of python and familiarity with web frameworks is assumed.

## Environments

Boutique can run in three different environments:

* Development
* Test
* Production

These environments has their own requirements file and settings file so you have
to make sure you are using the correct environment.


## Installing

Create a virtual environment and install the needed requirements

    $ mkvirtualenv boutique
    $ pip install -r requirements/development.txt


## Enable your environment

Run this in your shell to use the development settings:

    $ export DJANGO_SETTINGS_MODULE=boutique.settings.development

_This export can be handy to put in your venvs postactivate script_


## Setting up database

Development environment is using pythons built in sqlite support. All that
is needed is:

    $ python manage.py syncdb --migrate

Select Yes when prompted to create an account, and enter what you whish to use.


## Importing demo data

This step is optional, but if you want products in your shop, run this:

    $ python manage.py loaddata ../fixtures/catalogue.json


## Running

Run the local development server by issuing:

    $ python manage.py runserver

Now you should have a working server listening to port 8000 on your local
interface.


### Production

When running in production, more precaution is made, and you have to export
the projects secret as an environment variable, as well as selecting the
correct settings file

    $ export SECRET_KEY="-clxsvc7x0)%8is&4h0#acmpz91aszs%v-f29t893xf5g-@64z"
    $ export DJANGO_SETTINGS_MODULE=boutique.settings.development

Static files must be served by another entity than the Django application.
There is a management command to run to collect all static resources and put
those in another directory:

    $ python manage.py collectstatic

Then you should *NEVER EVER* use the debug server in production, instead run
django in a wsgi container using gunicorn or uwsgi

    $ gunicorn --log-file=boutique.log -b 127.0.0.1:8000 -D \
    -w 2 --pid boutique.pid boutique.wsgi:application
