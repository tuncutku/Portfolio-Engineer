#!/bin/bash

function activate { 
    echo "Activating env."
    source env/bin/activate
}

if [ -d "env" ]
then
    activate
else
    echo "Setting env up."
    python3 -m venv env
    activate
    echo "Installing requirements."
    pip3 install -q --upgrade pip
    pip3 install -q -r requirements.txt
fi

if [ "$1" == 'run_tests' ]
then
    echo "Running pytests."
    pytest --cov=src --cov-config=tests/.coveragerc --no-cov-on-fail -n auto
    echo "Running pylint on src/ and tests/"
    pylint src/
    pylint tests/
fi

if [ "$1" == 'init_db' ]
then
    export FLASK_APP=run_app.py
    echo "Initiating_db"
    flask init_db
fi

if [ "$1" == 'run_app' ]
then
    python3
fi