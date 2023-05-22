from user import User
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    canvasKey = os.getenv("CANVAS_KEY")
    notionToken = os.getenv("NOTION_TOKEN")
    notionPageId = os.getenv("NOTION_PAGE_ID")
    schoolAb = os.getenv("SCHOOL_URL")
    database_id = os.getenv("DATABASE_ID")
    test_user = User(canvasKey, notionToken, notionPageId, schoolAb, database_id)

    existing_assignments = test_user.notionProfile.getAssignments()

    # Get assignments from Canvas
    test_user.canvasProfile.set_courses_and_id()
    assignments_list = []
    for name in test_user.canvasProfile.list_classes_names():
        info = test_user.canvasProfile.get_assignment_objects(name, "upcoming")
        for new_assignment in info:
            if new_assignment["name"].lower() not in existing_assignments:
                assignment = {"class": name,
                              "date": new_assignment["due_at"],
                              "name": new_assignment["name"]}
                assignments_list.append(assignment)

    # Add to Notion
    # test_user.postDatabase(assignments_list)


if __name__ == "__main__":
    main()
