install:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt


upgrade:
	pip-compile --upgrade --max-rounds 20 requirements/prod.in
	pip-compile --upgrade --max-rounds 20  requirements/dev.in
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt


dep:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in
	pip install -r requirements/dev.txt
	pip install -r requirements/prod.txt

pipenv:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in
	pip install -r requirements.txt
	pipenv install -r requirements/prod.txt
	pipenv install --dev -r requirements/dev.txt

reset:
	rm -f apps/delta/migrations/0*.py
	./manage.py makemigrations
	rm -f db.sqlite3
	./manage.py migrate
	echo "from apps.users.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python manage.py shell

deploy:
	git push heroku master

createdb:
	psql -c "DROP DATABASE IF EXISTS delta;"
	psql -c "DROP USER IF EXISTS delta;"
	psql -c "CREATE DATABASE delta;"
	psql -c "CREATE USER delta WITH PASSWORD 'delta';"
	psql -c "ALTER ROLE delta SET client_encoding TO 'utf8';"
	psql -c "ALTER ROLE delta SET default_transaction_isolation TO 'read committed';"
	psql -c "ALTER ROLE delta SET timezone TO 'UTC';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE delta TO delta;"



pull_db:
	dropdb --if-exists delta
	heroku pg:pull DATABASE_URL delta --app deltacapital
	psql -d delta -c "REASSIGN OWNED BY ${USER} TO delta"

copy_to_dev:
	heroku pg:copy deltacapital::DATABASE_URL postgresql-sinuous-90885 --app deltacapital-dev --confirm deltacapital-dev



celery:
	celery -A config.celery_app worker --loglevel=info
	

mail:
	~/go/bin/MailHog
