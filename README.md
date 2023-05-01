
# Rest API Garden Store
This is a REST API created with Python and Django, using a MySQL database. The API was built for the Garden Store project, a web application for selling gardening products.

Technologies:
    - Python (Version 3.10.9)
    - Django with Django Rest Framework
    - Relational Database MySQL

# Dependencies Installation
To install the project dependencies, there is a file named requirements.txt attached. But first, you need to create a virtual environment with Python using the command:

    python -m venv env 

After running the command, a folder with the virtual environment will be created. To activate the virtual environment, run the activate.bat file located in env\Scripts\activate.bat. With the virtual environment activated, install the project dependencies using the command:

pip install -r requirements.txt

Afterwards, the dependencies for running the project will be installed.

# Migrations
To migrate the tables to the database, you need to first configure the settings.py file with the database connection details. Once you have done that, run the command:

    python manage.py makemigrations

This will create the migration files. Then, run the command:

    python manage.py migrate 

This will execute all the migrations and create the tables in the database.

# Execution
To run the project, activate the virtual environment with the installed dependencies and then run the command:

    python manage.py runserver (optional port number)
    
The port number is optional. If you do not provide a port number, the server will run on port 8000 at localhost.

