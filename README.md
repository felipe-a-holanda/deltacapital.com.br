# deltacapital.com.br



Install dependencies
```
sudo apt install direnv pipenv pip-tools postgresql postgresql-contrib python3-dev libpq-dev
direnv allow
```

Create Python virtualenv
```
export PIPENV_VENV_IN_PROJECT="enabled"
pipenv install -r requirements.txt
```


Update virtualenv
```
make
```


Compile frontend
```
npm install
npm run build
```


Run Django 
```
python manage.py migrate
python manage.py runserver
```