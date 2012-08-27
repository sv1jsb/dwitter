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

### Installation

#### Requirements

Apart from the requirements listed in _requirements.txt_ there are some extra:
* You must have redis installed on your system. Download the latest redis version from [redis.io](http://redis.io) and install it.
* The gevent version listed in requirements.txt is a development one and requires the latest [Cython](http://pypi.python.org/pypi/Cython/) to be installed. If you don't want that download gevent from [google code](http://code.google.com/p/gevent/downloads/list) and install it manually.

#### VirtualEnv

It's advised, but not necessary, to install all packages under a virtual python environment. Virtualenvwrapper is a collection of useful tools for virtualenv.

    pip install virtualenv virtualenvwrapper

Decide a name for the directory which will hold all your virtualenvs and add the next 3 lines at the end of your _.bashrc_

    export WORKON_HOME=~/venvs
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=~/venvs
    
and do:

    source ~/.bashrc
    
Now you are ready to create the environment you will work on.

    mkvirtualenv dwitter
    
Once created you can activate it by doing:

    workon dwitter
    
#### Download and install

Clone or fork this repository to a directory of your liking. Change directory to dwitter's root and do:

    pip install -r requirements.txt
    
This will download and install all requirements.

#### Configuration

Dwitter needs 5 servers to run in order to function correctly. That's why there is _servers_ directory containing all start/stop scripts and configuration files needed for those servers to work.
Those servers are configured to create all their needed files under the _servers_ directory. So there is no need for you to _sudo_. Start up scripts and local save are provided for redis also.
If this is not desired, in case you use redis already, you can delete this two lines from the _startall_ and _stopall_ scripts.

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

where you must provide the same path as in servers/servers.conf ENVPYTHON variable. 

