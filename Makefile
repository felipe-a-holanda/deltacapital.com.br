install:
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt


upgrade:
	pip-compile --upgrade --max-rounds 20 requirements/prod.in
	pip-compile --upgrade --max-rounds 20  requirements/dev.in
	cp requirements/prod.txt requirements.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt


dep:
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


pull_db:
	dropdb --if-exists delta
	heroku pg:pull DATABASE_URL delta --app deltacapital
	#psql -d delta -c "REASSIGN OWNED BY ${USER} TO delta"