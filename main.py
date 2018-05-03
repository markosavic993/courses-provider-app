from config import app
from dao import CourseDao
from api import *


def generate_data():
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


DAO = CourseDao()
generate_data()

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')