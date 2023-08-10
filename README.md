<!-- start -->
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

Add env file in uforangers dir

<!-- create migrations -->
python3 manage.py makemigrations
python3 manage.py migrate

<!-- collect static files -->
python3 manage.py collectstatic

<!-- run seed -->
python3 manage.py loaddata seed.json

<!-- run web server -->
python3 manage.py runserver

<!-- celery worker -->
celery -A uforangers worker -l INFO

<!-- db to seed -->
python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > new_data.json