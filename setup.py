from setuptools import setup

# Put here required packages
packages = [
    'django==1.6.1',
    'jinja2==2.7.2',
    'django-jinja',
    'coverage==3.7.1',
    'selenium==2.3.9',
    'django-selenium==0.9.6'
]

setup(name='Kno',
      version='1.0',
      description='Collaborative e-learning website',
      author='Matt Stark',
      author_email='mattstark75@gmail.com',
      url='',
      install_requires=packages,
)
