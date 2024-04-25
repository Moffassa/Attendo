# Attendo

Step 1: Run the virtual Environment:

source env/bin/activate

Step 2: Install all dependencies

pip install -r requirements.txt

Step 3: Change the databse variables in settings.py to your local postgresql variables (until we host a server for this)

Step 4: Run the migrations and create database

python3 manage.py makemigrations

python3 manage.py migrate

Step 4: Run the server

python3 manage.py runserver
