# Python in 1 minute

* Dynamic language
* Object oriented
* Functions are first class citizens
* Keep it simple

Python is far more than scripting. It is a quite competent general purpose
language.

Indentation matters, which is mainly a good thing.

---

# Python toolchain

* pip
* virtualenv
* gunicorn
* coverage
* pycharm

Toolchain is very unix, and since I use CPython you will get frustrated about
native packages every now and then.

Not as polished as Maven, but then again you will never need to see thousands
of lines of XML to declare your dependencies.

PEP8 is the style guide!

---

# Django

* MVC
* No. 1 web framework in Python
* Initial release 2005
* BSD Licensed

---

# Django features

* Templates
* Forms (validation, serialization)
* Middleware
* I18N, L10N
* Database backends (ORM)
* Admin backend
* Cache

---

# Anatomy of a django project

* What is a project?
* what is an app?
* How big should my apps be?
* Any third-parties out there?

---

# Django testing

* Coverage
* Mock and patch

Most Java people are scared due to the dynamic language, and they should be.
However, most of the risks can be mitigated by having good test coverage.

Go TDD-ish and test everything (cut templates if you need)

---

# Django models

* Just python code
* ORM
* Supports spanning between models
* Reverse relations
* Can be abstract to allow mixins
* Fat models

Can sometimes be too fat.

--

# Django settings

* Just python code
* Local settings considered anti-pattern
* Use one for each environment
    - settings/development.py
    - settings/production.py
* Export DJANGO_SETTINGS_MODULE

    $ export DJANGO_SETTINGS_MODULE=boutique.settings.development

---

# Django routing

* Just python code
* Specify URL's using regexp
* Decoupled from views by name and arguments
* Avoid complexity

---

# Django templates

* Curly FTW
* Works on context from view
* Python-ish syntax
* Allow custom filter and tags
* Keep it simple - complexity grows fast
* Beware of Django models and hidden queries

Don't try to be smart. Code reuse is not everything, better to take the hit
with duplicate markup than ubercomplex templating.

---

# Django views

* Class based views
* Function based views
* Generic views
    - Great for CRUD
* Choose what you need and mix freely
* Use mixins!

Don't be afraid to have many views, beats branching anyway

---

# Django forms

* Just python code
* Forms validate data
* Forms can render
     - Although default render is stupid (validation above fields anyone?)
* Supports models

Learn forms, it makes for good separation of concern.

Rendering most likely needs to be customised though.

---

# Django Admin

* Generated UI for dealing with models
* Really powerful
* Looks like it's 2005 again
* This feature alone makes it interesting
* For power users, admins, not end-users

Avoid customizing yourself, there are third-party plugins.

---

# Database migrations

* South is a database migration plugin
    - Will be default in Django 1.7
* Allow your models to grow in a controlled way
* Schema migration
* Data migration


---

# Initial migrations

Activate South when you are happy with your models

    python manage.py schemamigration catalogue –initial

This will setup the baseline for each model.

It's just python code, noting magic.

---

# Schema migration

* Make the needed changes your model(s)
* Run south to generate migration
* Apply migration
* It is only python code


    $ python manage.py schemamigration catalogue --auto
    $ python manage.py migrate catalogue

You will automatically get code to perform forward / reverse.

South keeps track on which that has run for current database.

---

# Data migration

* When data needs to be changed in models
* Field additions / removal
* Is just python code


    $ python manage.py datamigration catalogue craft_beer
    $ python manage.py migrate catalogue

Will generate a skeleton for you to implement.

---

# Fixtures

* JSON version of models
* Useful for test data
* Useful for migrating (small sets of) data between database types
* Avoid for unit tests (slow and fragile)

---

# Generate fixtures

* Generate fixtures (JSON) from Models
* Supports XML as well


    $ python manage.py dumpdata catalogue > ../fixtures/catalogue.json

---

# Load fixtures

* Load fixtures from file
* Can be run multiple times


    $ python manage.py loaddata ../fixtures/catalogue.json

---

# Django shell

* A REPL with access to all your code (read models)
* Very good for debugging (it is available in production)
* Very handy for model queries
* NO replacement for unit tests

Install bpython in your venv and you will get docs and tab completion.

    from checkout.models import Cart
    for cart in Cart.objects.all():
        for ci in cart.items.all():
            print "%s %s" % (ci.quantity, ci.product.title)


    [c.total_price for c in Cart.objects.all()]

---

# Django translations

* String translations
* Based on GNU gettext utility
* Supports more than 1:1 strings


---

# Django debug toolbar

Awesome third party plugin.

* Statistics
* Profiling
* Context
* Cache hits / misses

---

# Strengths

* Dynamic language
* Productive
* ORM
* Admin mode (for simple sites)

---

# Weaknesses

* Dynamic language
* Single threaded (by default)
* Performance is not great

But not all apps are Facebook...

---

# Thank you!
