django-diazo-blog
=================

Example implementation of Diazo in Django

Clone the repo

    git clone git@github.com:Goldmund-Wyldebeast-Wunderliebe/django-diazo-blog.git
    cd django-diazo-blog

Create and enable a virtualenv

    virtualenv .
    source bin/activate

Install Django

    pip install -r requirements.txt

Configure Django

    python manage.py syncdb --all
    python manage.py migrate --fake
    python manage.py collectstatic
    python manage.py syncthemes

    python manage.py runserver

Go to the Django Admin interface and enable the Ministerial theme (with debug).
Go to the main Django application

