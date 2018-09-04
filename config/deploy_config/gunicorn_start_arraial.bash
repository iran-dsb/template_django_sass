#!/bin/bash
NAME="template_sass" #Name app
DJANGODIR=/home/webapps/template_sass/current/template_sass
SOCKFILE=/home/webapps/template_sass/run/gunicorn.sock  # we will communicte using
NUM_WORKERS=9                                     # how many worker processes
DJANGO_SETTINGS_MODULE=template_sass.settings_production             # which settings file should
DJANGO_WSGI_MODULE=template_sass.wsgi                     # WSGI module name

# Activate the virtual environment
cd $DJANGODIR
source /home/webapps/template_sass/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do
# not use --daemon)
exec /home/webapps/template_sass/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $NAME \
	--workers $NUM_WORKERS \
	--bind=unix:$SOCKFILE \
	--log-level=debug \
	--log-file=-
