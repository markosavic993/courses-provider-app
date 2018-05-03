from flask import Flask
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="Courses API", description="API that supports CRUD operations for courses and it's attendees.")
ns = api.namespace('courses', description='Courses operations')
