from config import api


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