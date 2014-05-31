Kno
--------------------
A collaborative e-learning website

Installation
---------
First you will need to install the setuptools module for python3. For a debain based system, this will work
```bash
sudo apt-get install python3-setuptools
```

The following code will install and run kno correctly on a debian based system
```bash
sudo python3 setup.py install
python3 manage.py syncdb --noinput
python3 manage.py loaddata data  # loads initial data - not nessecary, but nice to have
python3 manage.py runserver
```

In order to reset the server data, in case something happens, or you change your models.
```bash
rm db.sqlite3 && python3 manage.py syncdb && python3 manage.py loaddata data
```

Conversely, after you've made your models, if you need to dump the data to a fixture so it's
automatically loaded
```bash
python3 manage.py dumpdata -e contenttypes --indent 4 > common/fixtures/data.json
```

Requirements (installed through setup.py):
---------
* python 3.3 (3.2 is not supported by jinja2)
* django 1.6.1
* jinja2
* django-jinja
* selenium 2.3.9
* django-mpdd 0.6.1


Testing:
---------
To test, run this command
```bash
python3 manage.py runserver
```

If you want to get a report of the tests, run this command instead
```bash
coverage run manage.py test -v 2 && coverage html $(find . | grep ".py$" | egrep -v "test|setup|middleware")
```
