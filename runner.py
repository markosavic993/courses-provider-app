from app import app, api
from app.example import CoursesList, Course

api.add_resource(CoursesList, '/courses')
api.add_resource(Course, '/courses/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)