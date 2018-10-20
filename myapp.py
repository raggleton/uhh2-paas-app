#!/usr/bin/env python

"""App to listen for github events, and carry out a corresponding task e.g. push to gitlab

NB if you rename this file to `app.py` in the future, you'll need to set 
`APP_FILE` in openshift to null otherwise it'll run this instead of gunicorn:
https://github.com/sclorg/s2i-python-container/issues/190
"""


from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello. This is your app."


if __name__ == '__main__':
    app.run()