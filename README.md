# Dwitter
### A Twitter clone written in django

Dwitter is made by different apps and modules available for django and python. It uses:

* Gunicorn
* Gevent
* Gevent-socketio
* Redis
* Celery
* Haystack
* django-taggit
* django-registration

### Features

* User registration
* User profile with name, description and image
* Multilingual, user selectable
* User search in name and description using haystack
* User notification when new _dwit_ arrives
* Direct, Reply and Redwit capability
* Hash tags, tag search and tag watch

### Purpose

Dwitter is an educational and experimental project. It shows how one can combine different modules and apps available for python and django in order to make an application like twitter. It uses websockets, distributed task queue, ajax calls and redis in order to achieve this.

### Installation

#### Requirements

Apart from the requirements listed in _requirements.txt_ there are some extra:
* You must have redis installed on your system. Download the latest redis version from [redis.io](http://redis.io) and install it.
* The gevent version listed in requirements.txt is a development one and requires the latest [Cython](http://pypi.python.org/pypi/Cython/) to be installed. If you don't want that download gevent from [google code](http://code.google.com/p/gevent/downloads/list) and install it manually. You can find a wiki [page](https://github.com/sv1jsb/dwitter/wiki/Cython-installation) for Cython installation.

#### VirtualEnv

It's advised, but not necessary, to install all packages under a virtual python environment. Virtualenvwrapper is a collection of useful tools for virtualenv.

    pip install virtualenv virtualenvwrapper

Decide a name for the directory which will hold all your virtualenvs and add the next 3 lines at the end of your _.bashrc_. (Here ~/venvs is given as 

    export WORKON_HOME=~/venvs
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=~/venvs
    
and do:

    source ~/.bashrc
    
Now you are ready to create the environment you will work on.

    mkvirtualenv dwitter
    
Once created you can activate it with:

    workon dwitter
    
#### Download and install

Clone or fork this repository to a directory of your liking. Change directory to dwitter's root and do:

    pip install -r requirements.txt
    
This will download and install all requirements.

#### Configuration

Dwitter needs 5 servers to run in order to function correctly. That's why there is a _servers_ directory containing all start/stop scripts and configuration files needed for those servers to work.
Those servers are configured to create all their needed files under the _servers_ directory. So there is no need for you to _sudo_. Start up scripts and local database dump are provided for redis also.
If this is not desired, in case you use redis already, you can delete this two lines from the _startall_ and _stopall_ scripts. There is also a wiki [page](https://github.com/sv1jsb/dwitter/wiki/Redis-setup) for redis setup.

##### servers/servers.conf

This file holds all the necessary variables for _celery_. Change the following variables to suit your case:

    # Full path to root location of project
    CEL_CHDIR=path/to/dwitter's root
    
    # Full path of virtualenv or system interpreter
    ENVPYTHON=path/to/python
    
    # Username ang group the celery servers will run under.
    SERVERS_USER = youruser
    SERVERS_GROUP = yourgroup

##### servers/redis.conf

Configuration file for local redis server. Change the following variables to suit your case:

    # Full path of redis pid file. Recomendation: (dwitter_root)/servers/run/redis.pid
    pidfile path/to/redis.pid
    
    # Full path of redis log file. Recomendation: (dwitter_root)/servers/log/redis.log
    logfile path/to/redis.log
    
    # Full path of redis db directory. Recomendation: (dwitter_root)/servers/redis
    dir path/to/redis_db_dir

##### dwitter/settings.py

The only necessary variable here is:

    PYTHON_ENV = 'path/to/python'

where you must provide the same path as in servers/servers.conf ENVPYTHON variable. For a complete list of variables available in settings.py please visit the wiki [page](https://github.com/sv1jsb/dwitter/wiki/Settings.py-variables).

#### First time setup

Once everything is installed you must setup the database, change directory to dwitter's root (if not already there) and type the following commands:

    ./manage.py syncdb                           # To create your db
    ./manage.py createsuperuser                  # To create your first user
    ./manage.py migrate djcelery                 # This is needed for celery
    ./manage.py convert_to_south dwitter.main    # This is optional but useful
    ./manage.py collectstatic                    # To have your static files ready for serving
    ./manage.py rebuild_index                    # To create your haystack db

You are now ready to start the servers.

    servers/startall

This will start redis, celery, celeryev, celerybeat. To stop the servers do:

    servers/stopall

Every server can be started/stopped by its own with its starting script:

    servers/celeryd start
    etc.

In order to start gunicorn you have two options.

Either run it with:

    ./manage.py run_gunicorn -c gunicorn

this will start the gunicorn server with the ./gunicorn file as config displaying the log at your console.

Or:

    servers/gu start

this will start the gunicorn server with the servers/gunicorn file as config which daemonizes it and saves logs at servers/log/gunicorn.log. In order to stop the server you need to do:

    servers/gu stop

#### First time run

Once everything is running point you browser to: *127.0.0.1:8000/* and test it.

Dwitter's members have an one to one relation with django users. So when creating a user you must first create a django user, and then create a new member and relate it with the user just created.

So go to admin page login with the superuser data you provided earlier and create a member for the superuser.

Now you can login and use dwitter. Phew!!

Enjoy!!

### Links

This project was inspired by Flavio Curella's blog [post](http://curella.org/blog/2012/jul/17/django-push-using-server-sent-events-and-websocket/) and a series of blog posts by Rick Copeland and especially [this](http://blog.pythonisito.com/2012/07/realtime-web-chat-with-socketio-and.html).

Software used:

* [Celery](http://celeryproject.org)
* [Redis](http://redis.io)
* [Haystack](http://haystacksearch.org)
* [Gunicorn](http://gunicorn.org)
* [Gevent](https://bitbucket.org/denis/gevent)
* [Gevent-socketio](http://bitbucket.org/denis/gevent)
* [django-registration](https://bitbucket.org/ubernostrum/django-registration)
* [django-taggit](https://github.com/alex/django-taggit)
* [Twitter text lib](https://github.com/twitter/twitter-text-js)
* [Bootstrap](http://twitter.github.com/bootstrap)



