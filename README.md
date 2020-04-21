# Multi DB Router Application


## Requirements with Versions (Ubuntu)
	Django==1.10
	django-mysql==2.1.0
	dnspython==1.16.0
	mysql-connector-python==8.0.19
	MySQL-python==1.2.5
	protobuf==3.6.1
	psycopg2==2.8.5
	PyMySQL==0.9.3
	pytz==2019.3
	six==1.14.0


### To install requirements dependecies,please run the following command :
		pip install -r requirements.txt


## Configure Settings :

	Their are separate settings files for local,staging and production environments in multi_db_router project folder and can be used in the multi_db_router project by specifying settings file name in manage.py file.

## Database details :

	Database settings is configured in settings.py file with following details :
	- database1,database2 of PostgreSQL database.
	- database3,database4,database5 of MySQL database.

## After configuration of project settings, please run command :

	- To create migration file in migration folder, run command :
		python manage.py makemigrations

	- To migrate the changes in the databases, please run the command :	
		python manage.py migrate # It will migrate changes in the default database

	- To migrate the database changes in to specific database, please run the following command :
		python manage.py migrate --database=<database_name>
		- Example :
			python manage.py migrate --database=database1


## Server Setup
	
	Please run the following command to run the server :

		- python manage.py runserver ip address:port

		By default if no ip address is specified then it will run on local host and url will be :
  			http://127.0.0.1:8000/

		If ip address is specified is 172.XX.X.XXX and port is 8000 , then project url will be :
  			http://172.XX.X.XXX:8000/


## References :

	- https://docs.djangoproject.com/en/1.10/
	- https://docs.djangoproject.com/en/1.10/topics/db/multi-db/
	- https://www.postgresql.org/docs/
	- https://dev.mysql.com/doc/


## Points Need to be taken care of:

	Please installl the required libraries with proper version, It is recommended to install dependencies in virtual environment to avoid dependencies version confilts.
	To install virtual environment,please refer https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/