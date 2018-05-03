from flask_restplus import Resource

from main import DAO
from config import api, ns
from model import course, attendee


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