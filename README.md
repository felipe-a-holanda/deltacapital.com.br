# deltacapital.com.br



Install dependencies
```
sudo apt install direnv pipenv pip-tools postgresql postgresql-contrib python3-dev libpq-dev

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
pipenv install -r requirements.txt
direnv allow
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


Create database
```
cp .env.example .env
python manage.py migrate
```



Run Django server
```
python manage.py runserver
```