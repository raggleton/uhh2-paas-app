#!/usr/bin/env python

"""App to listen for github events, and carry out a corresponding task e.g. push to gitlab

NB if you rename this file to `app.py` in the future, you'll need to set 
`APP_FILE` in openshift to null otherwise it'll run this instead of gunicorn:
https://github.com/sclorg/s2i-python-container/issues/190
"""


import sys
import logging
from flask import Flask, request
from subprocess import check_call


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)


@app.route("/gitlab-forward", methods=["GET", "POST"])
def gitlab_forwarder():
    """Handle an incoming POST from github, do something to gitlab"""
    app.logger.info(request)
    request_json = request.get_json()
    app.logger.info(request_json)

    action = request_json["action"]

    pr_num = request_json["number"]
    base_branch = request_json["pull_request"]["base"]["ref"]
    proposer = request_json["pull_request"]["user"]["login"]
    app.logger.info("Handling PR %d from %s, to merge into branch %s. PR was %s." % (pr_num, proposer, base_branch, action))

    should_run_actions = ["opened", "reopened", "labeled"]
    if action not in should_run_actions:
        return 'Doing nothing'

    app.logger.info("Pushing to gitlab")
    check_call(['./testPush', str(pr_num), base_branch])

    return 'Forwarding to gitlab'


@app.route('/')
def index():
    return "Hello. This is your app."


if __name__ == '__main__':
    app.run()