#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "HERE!!!Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"

    # Command out when persistent data is implemented
    echo "Creating the database tables..."
    python manage.py create_db
    echo "Tables created"
fi

if [ "$FLASK_DEBUG" = "1" ] 
then
    echo "Creating the database tables..."
    python manage.py create_db # create a new table and wipe out old one
    echo "Tables created"
fi

exec "$@"