# my_sample_code

## Pre-requisites
 - python3.8
 - python3.8-venv
 - postgresql

## Installation

Create a new directory to work in, and cd into it:
```
mkdir <folder_name>
cd <folder_name>
```
Clone the project:
```
https://github.com/AleksandrPischulin/my_sample_code.git
```
Create and activate a virtual environment:
```
python3.8 -m venv venv
source venv/bin/activate
```
cd into my_sample_code folder:
```
cd my_sample_code
```
Update pip inside the virtual environment and install project requirements:
```
pip install --upgrade pip
pip install -r requirements.txt
```
## Config
Create a new psql database and user:
```
sudo -u postgres psql
postgres=# create database mydb;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database mydb to myuser;
```
in my_sample_code folder create new file secret_settings.py and add the following information to it:
```
SECRET_KEY = 'some_secret_string'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your created db name'
        'USER': 'your created user name',
        'PASSWORD': 'your created user password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

```
Run migrations:
```
python manage.py migrate
```
Run dev-server:
```
python manage.py runserver
```
