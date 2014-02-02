Collaborative e-learning website

First you will need to install the setuptools module for python3. For a debain based system, this will work
```bash
sudo apt-get install python3-setuptools
```

The following code will install and run kno correctly on a debian based system
```bash
sudo python3 setup.py install
python3 manage.py syncdb --noinput
python3 manage.py runserver
```

Requirements:
---------
* python 3
* django 1.6.1
* jinja2
* django-jinja


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
