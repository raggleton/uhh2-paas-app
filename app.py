#!/usr/bin/env python

"""App to listen for github events, and carry out a corresponding task e.g. push to gitlab"""


from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello. This is your app."


if __name__ == '__main__':
    app.run()