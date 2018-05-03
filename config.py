from flask import Flask
from flask_restplus import Api
from flask_basicauth import BasicAuth
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'coursesinfoapi'
app.config['BASIC_AUTH_PASSWORD'] = 'tester11'
basic_auth = BasicAuth(app)

app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['BASIC_AUTH_FORCE'] = True

api = Api(app, version="1.0", title="Courses API", description="API that supports CRUD operations for courses and it's attendees.")

ns = api.namespace('courses', description='Courses operations')
