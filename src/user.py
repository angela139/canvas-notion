from canvas import CanvasApi
from notion import NotionApi


class User:
    def __init__(
        self,
        canvasKey,
        notionToken,
        notionPageId,
        schoolAb,
        database_id=None,
    ):
        self.notionToken = notionToken
        self.database_id = database_id
        self.canvasProfile = CanvasApi(canvasKey, schoolAb)
        self.page_ids = {"Default": notionPageId}
        self.generated_db_id = None
        self.schoolAb = schoolAb
        self.notionProfile = NotionApi(
            notionToken,
            database_id=database_id,
            schoolAb=schoolAb,
        )

    # Shorthand fucntion for getting list of courses that started within the past 6 months from Canvas
    def getCoursesLastSixMonths(self):
        return self.canvasProfile.get_courses_within_six_months()

    # Shorthand function for getting list of all courses from Canvas
    def getAllCourses(self):
        return self.canvasProfile.get_all_courses()

    def getDatabase(self):
        return self.notionProfile.getAssignments()

    def postDatabase(self, assignments):
        self.notionProfile.addAssignments(assignments)

