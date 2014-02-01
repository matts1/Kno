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
