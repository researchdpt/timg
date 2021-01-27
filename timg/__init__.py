from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask import Flask
from flask.views import MethodView

import uuid, time, os, time, re, signal
import pkg_resources, platform
import humanize

app = Flask(__name__)
app.jinja_env.cache = {}
app.config.update(dict(
    SECRET_KEY="NOTNEEDED"
))
import timg.initialize
