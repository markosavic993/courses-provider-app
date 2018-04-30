from app import app, api
from flask_restful import Resource, Api

# ns = api.namespace("/courses", description="Operations related to courses.")

# @ns.route("/courses")
class CoursesList(Resource):
    def getAll(self):
        """

        :return: list of courses
        """
        return {'hello': 'world'}

# @ns.route("/<int:id>")
class Course(Resource):
    def getById(self, id):
        """

        :param id:  id of the course - numeric value containing 5 elements
        :return: course with given id
        """
        return {'id': 55555}