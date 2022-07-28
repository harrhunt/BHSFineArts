#! /usr/bin/fish

set -x FLASK_APP bhs.py
set -x FLASK_ENV development
python -m flask run