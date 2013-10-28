pip install -r requirements.txt
mkdir logs/
python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py collectstatic --link --noinput
python manage.py syncthemes
