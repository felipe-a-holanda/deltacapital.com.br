# deltacapital.com.br

Install dependencies

```
sudo apt install direnv pipenv postgresql postgresql-contrib python3-dev python3-pip
pip3 installl pip-tools
```

Add this to ~/.bashrc

```
# direnv:
eval "$(direnv hook bash)"
show_virtual_env() {
  if [[ -n "$VIRTUAL_ENV" && -n "$DIRENV_DIR" ]]; then
    echo "($(basename $VIRTUAL_ENV))"
  fi
}
export -f show_virtual_env
PS1='$(show_virtual_env)'$PS1

```

Create Python virtualenv

```
export PIPENV_VENV_IN_PROJECT="enabled"
pipenv install
pip install -r requirements.txt
pip install -r requirements/dev.txt
direnv allow
```

Update virtualenv

```
make
```

Compile frontend

```
npm install
npm run start 
```

Create database

```
cp .env.example .env
python manage.py migrate
```

Create admin user
```
./manage.py createsuperuser
```

Run Django server

```
python manage.py runserver
```
