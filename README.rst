
This is a sample API project based on Django REST framework for PyconFR 2016.

To execute the code::

 git clone https://github.com/bleemeo/mypublicapi.git
 mkvirtualenv mypublicapi
 pip install -r requirements.txt
 python manage.py migrate
 python manage.py createsuperuser

Run the application::
 python manage.py runserver

Open your browser and go to http://localhost:8000/admin to login

Then you can browse the API at http://localhost:8000/v1/

To create a server using cURL::

 curl -X POST -u username -H 'Content-Type: application/json' \
 -d '{"name": "myserver", "properties": [{"name": "OS", "value": "Linux"}, {"name": "CPU", "value": "i7 5500U"}]}' \
 http://localhost:8000/v1/server/

