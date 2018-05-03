from flask_restplus import fields

from config import api

attendee = api.model("Attendee", {
    "attendeeId": fields.Integer(readOnly=True, description="The unique identifier of attendee."),
    "firstName": fields.String(required=True, description="First name of the attendee"),
    "lastName": fields.String(required=True, description="Last name of the attendee"),
    "email": fields.String(required=True, description="Email address of the attendee")
})
course = api.model('Course', {
    'id': fields.Integer(readOnly=True, description="The course unique identifier - numeric value containing at least 5 digits"),
    'name': fields.String(required=True, description="The name of the course"),
    'description': fields.String(required=False, description="Description of the course"),
    "instructor": fields.String(required=True, description="Name of the instructor"),
    "attendees": fields.List(fields.Nested(attendee), equired=False, description="List of the attendees for given course")
})