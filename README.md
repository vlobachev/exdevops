# Simple app

### App that should be deployed

That is a super service that is very important for our business.
We wrote this service in python3.8 programming language and we used [django](https://www.djangoproject.com/) as a web framework. 


#### How to run service locally (for developers):

1) Install python 3.8
2) Create [virtual env](https://docs.python.org/3/tutorial/venv.html) if you like to isolate your environment ()
3) Install all packages for project `pip install -r requirements/main.txt`
4) Install all packages for development `pip install -r requirements/dev.txt`
5) Create a local database (SQLite) and apply all migrations by `./manage.py migrate`
6) Run dev server `./manage.py runserver`

#### Entrypoints

```shell script
# simple ping 
curl http://localhost:8000/-/ping/  

# Check that app works correctly
curl http://localhost:8000/-/status/

# Metrics entrypoint for Prometheus
curl http://localhost:8000/-/metrics
```

### Development
 We use a few of checks before code goes to master:
 ```shell script
LENGTH=120
# Unit tests
pytest -v --cov=src -v --cov-report=xml --cov-report=term
# Code complexity and gidelines
pylint src tests --reports=n --max-line-length=$(LENGTH) --output-format=text
pycodestyle src tests --max-line-length=$(LENGTH) --format pylint --exclude=migrations --ignore=E203,W503
# Python imports ordering
isort --lines $(LENGTH) -vb -rc --check-only -df src tests
# Code formating 
black --check --diff -v -l $(LENGTH) src tests

# ALL together
make checks
```


### Production 
1) The application should run on Linux Server
2) It should be served by a WSGI server. Read how to deploy Django app [here](https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/)
3) The app should be run with environment value APP_CONFIG_PATH=./configs/prod.env
4) Use Postgres as database (DSN psql://user:password@db/app?application_name=simple_app) 
5) Use Redis as Cache


Check your deploy with a status entry point and wrk (or other benchmark tool)