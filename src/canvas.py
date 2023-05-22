import requests, json
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from requests.auth import HTTPBasicAuth
import pytz


class Class:
    def __init__(self, id=None, name=None, term_id=None, assignments=None):
        self.id = id
        self.name = name
        self.assignments = []
        self.term_id = term_id


# Class implementation of canvas API
class CanvasApi:
    def __init__(self, canvasKey, schoolAb=""):
        self.canvasKey = canvasKey
        self.schoolAb = schoolAb
        self.header = {"Authorization": "Bearer " + self.canvasKey}
        self.courses = {}

    def get_all_courses(self):
        params = {
            "per_page": 200,
            "include": ["concluded"],
            "enrollment_state": ["active"],
        }
        readUrl = f"https://{self.schoolAb}/api/v1/courses"
        classes = []
        courses = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()

        for i in courses:
            if i.get("name") != None:
                name = i.get("name")
                name = cleanCourseName(name)

                classObj = Class(
                    i.get("id"),
                    name,
                    i.get("enrollment_term_id"),
                    i.get("assignments"),
                )
                classes.append(classObj)
        return classes

    # Initialize self.courses dictionary with the key being
    def set_courses_and_id(self):
        for courseObject in self.get_all_courses():
            if courseObject != None:
                self.courses[courseObject.name] = courseObject.id

    # Return a courses id number given the courses name
    def get_course_id(self, courseName):
        return self.courses[courseName]

    # Returns a list of all assignment objects for a given course
    def get_assignment_objects(self, courseName, timeframe=None):
        readUrl = f"https://{self.schoolAb}/api/v1/courses/{self.courses[courseName]}/assignments/"
        params = {"per_page": 500, "bucket": timeframe}

        assignments = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()
        assignmentList = []

        for assignment in assignments:
            utc_time_string = assignment["due_at"]
            # Create a datetime object from the UTC time string
            utc_datetime = datetime.strptime(utc_time_string, '%Y-%m-%dT%H:%M:%SZ')

            # Set the UTC timezone for the datetime object
            utc_timezone = pytz.timezone('UTC')
            utc_datetime = utc_timezone.localize(utc_datetime)

            # Convert the datetime object to Pacific Time
            pacific_timezone = pytz.timezone('US/Pacific')
            pacific_datetime = utc_datetime.astimezone(pacific_timezone)

            # Format the Pacific Time as a string
            pacific_time_string = pacific_datetime.strftime('%Y-%m-%d %H:%M:%S')
            assignment["due_at"] = pacific_time_string
            assignment["url"] = assignment["html_url"]
            assignmentList.append(assignment)

        return assignmentList

    def list_classes_names(self):
        class_list = []
        for course in self.get_all_courses():
            class_list.append(course.name)
        return class_list


def cleanCourseName(name):
    cleanName = ""
    num = 0

    if name != None:
        name = name.replace(" ", "")

    while name[num].isalpha() or name[num] == "/" or name[num] == "-":
        cleanName += name[num]

        if name[num] == name[-1]:
            break

        num += 1

    while name[num].isdigit() and num < 6:
        cleanName += name[num]

        if name[num] == name[-1]:
            break

        num += 1
    return cleanName
