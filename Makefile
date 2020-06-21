install:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in
	cp requirements/prod.txt requirements.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt

pipenv:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in
	cp requirements/prod.txt requirements.txt
	pip install -r requirements.txt
	pipenv install -r requirements/prod.txt
	pipenv install --dev -r requirements/dev.txt

reset:
	rm -f apps/delta/migrations/0*.py
	./manage.py makemigrations
	rm -f db.sqlite3
	./manage.py migrate
	echo "from apps.users.models import User; User.objects.create_superuser('admin', 'admin@oowlish.com', 'admin')" | python manage.py shell

deploy:
	git push heroku master