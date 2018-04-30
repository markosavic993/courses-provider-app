from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="Courses API", description="API that supports CRUD operations for courses and it's attendees.")

ns = api.namespace('courses', description='Courses operations')

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

class CourseDao(object):
    def __init__(self):
        self.counter = 10000
        self.courses = []

    def get(self, id):
        for course in self.courses:
            if course['id'] == id:
                return course
        api.abort(404, "Course {} doesn't exist".format(id))

    def create(self, data):
        course = data
        course["id"] = self.counter = self.counter + 1
        self.courses.append(course)
        return course

    def update(self, id, data):
        course = self.get(id)
        course.update(data)
        return course

    def delete(self, id):
        course = self.get(id)
        self.courses.remove(course)

    def getAttendee(self, courseId, attendeeId):
        course = self.get(courseId)
        for attendee in course["attendees"]:
            if attendee["attendeeId"] == attendeeId:
                return attendee
        api.abort(404, "Attendee {} doesn't exist".format(attendeeId))

    def addAttendee(self, courseId, data):
        attendee = data
        attendee["attendeeId"] = self.counter = self.counter + 1
        course = self.get(courseId)
        course.attendees.append(attendee)
        return course

    def updateAttendee(self, courseId, attendeeId, data):
        attendee = self.getAttendee(courseId, attendeeId)
        attendee.update(data)

    def removeAttendee(self, courseId, attendeeId):
        course = self.get(courseId)
        course.attendees.remove(self.getAttendee(courseId, attendeeId))


DAO = CourseDao()
DAO.create({"name": "Typescript",
            "instructor": "Janko Sokolovic",
            "description": "A beginers guide to Typescript usage and migration from Angular JS.",
            "attendees": [{
                "attendeeId": 123,
                "firstName": "Marko",
                "lastName": "Savic",
                "email": "Marko.Savic@zuhlke.com"
            },
                {
                "attendeeId": 124,
                "firstName": "Mihailo",
                "lastName": "Matijevic",
                "email": "Mihailo.Matijevic@zuhlke.com"
            },
                {
                "attendeeId": 125,
                "firstName": "Petar",
                "lastName": "Misic",
                "email": "Petar.Misic@zuhlke.com"
            }]})

DAO.create({"name": "Docker",
            "instructor": "Janko Sokolovic",
            "description": "An introduction workshop to Docker with hadn practical approach.",
            "attendees": [{
                "attendeeId": 126,
                "firstName": "Marko",
                "lastName": "Savic",
                "email": "Marko.Savic@zuhlke.com"
            },
                {
                "attendeeId": 127,
                "firstName": "David",
                "lastName": "Miric",
                "email": "David.Miric@zuhlke.com"
            },
                {
                "attendeeId": 128,
                "firstName": "Marko",
                "lastName": "Milinkovic",
                "email": "Marko.Milinkovic@zuhlke.com"
            }]})


@ns.route('/')
class CourseList(Resource):
    '''Shows a list of all courses, and lets you POST to add new courses'''
    @ns.doc('list_courses')
    @ns.marshal_list_with(course)
    def get(self):
        '''List all courses'''
        return DAO.courses

    @ns.doc('create_course')
    @ns.expect(course)
    @ns.marshal_with(course, code=201)
    def post(self):
        '''Create a new course'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, "Course not found")
@ns.param('id', 'The course identifier')
class Course(Resource):
    '''Show a single course item and lets you update and delete them'''
    @ns.doc('get_course')
    @ns.marshal_with(course)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc("delete_course")
    @ns.response(204, "Course deleted")
    def delete(self, id):
        '''Delete a course given its identifier'''
        DAO.delete(id)
        return "", 204

    @ns.doc("update_course")
    @ns.expect(course)
    @ns.marshal_with(course)
    def put(self, id):
        '''Update a course given its identifier'''
        return DAO.update(id, api.payload)

@ns.route("/<int:id>/attendees")
@ns.response(404, "Course not found")
@ns.param('id', 'The course identifier')
class AttendeeList(Resource):
    """
        Show list of all the attendees for the given course and gives you an option to add new attendee for the course
    """

    @ns.doc("list_attendees")
    @ns.marshal_list_with(attendee)
    def get(self, id):
        """
        :return: Fetch attendees for given course
        """
        return DAO.get(id).courses

    @ns.doc("add_attendee")
    @ns.expect(attendee)
    @ns.marshal_with(attendee, 201)
    def post(self, id):
        """
        :return: add attendee for for given course
        """
        return DAO.addAttendee(id, api.payload)

@ns.route('/<int:id>/attendees/<int:attendeeId>')
@ns.response(404, 'Attendee or course not found')
@ns.param('id', 'The course identifier')
@ns.param('attendeeId', 'The attendee identifier')
class Attendee(Resource):
    """
        Show single attendee for given course and lets you update and delete them
    """

    @ns.doc("get_attendee")
    @ns.marshal_with(attendee)
    def get(self, id, attendeeId):
        """
        :return: Fetch attendee for given id from choses course
        """
        return DAO.getAttendee(id, attendeeId)

    @ns.doc("delete_attendee")
    @ns.response(204, "Attendee removed for given course")
    def delete(self, id, attendeeId):
        """
        :return: Delete an attendee given its identifier from chosen course
        """
        DAO.removeAttendee(id, attendeeId)
        return "", 204

    @ns.doc("update_attendee")
    @ns.expect(attendee)
    @ns.marshal_with(attendee)
    def put(self, id, attendeeId):
        """
        :return: Update an attendee given its identifier from chosen course
        """
        DAO.updateAttendee(id, attendeeId)

if __name__ == '__main__':
    app.run(debug=True)