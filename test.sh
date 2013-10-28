reset
mkdir logs
pip install selenium==2.35.0
./manage.py syncdb --all --noinput
./manage.py migrate --fake --noinput
./manage.py collectstatic --link --noinput
./manage.py test diazo_blog --traceback -v 3
