from user import User
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    canvasKey = os.environ["CANVAS_KEY"]
    ccsfKey = os.environ["CCSF_KEY"]
    notionToken = os.environ["NOTION_TOKEN"]
    notionPageId = os.environ["NOTION_PAGE_ID"]
    schoolAb = os.environ["SCHOOL_URL"]
    ccsfAb = os.environ["CCSF_URL"]
    database_id = os.environ["DATABASE_ID"]
    ucdavis_user = User(canvasKey, notionToken, notionPageId, schoolAb, database_id)
    ccsf_user = User(ccsfKey, notionToken, notionPageId, ccsfAb, database_id)

    existing_assignments = ucdavis_user.notionProfile.getAssignments()

    # Get assignments from Canvas for UC Davis
    ucdavis_user.canvasProfile.set_courses_and_id()

    assignments_list = []

    for name in ucdavis_user.canvasProfile.list_classes_names():
        info = ucdavis_user.canvasProfile.get_assignment_objects(name, "upcoming")
        for new_assignment in info:
            if new_assignment["name"].lower() not in existing_assignments:
                assignment = {"class": name,
                              "date": new_assignment["due_at"],
                              "name": new_assignment["name"]}
                assignments_list.append(assignment)

    # Get assignments from Canvas for CCSF
    ccsf_user.canvasProfile.set_courses_and_id()
    for name in ccsf_user.canvasProfile.list_classes_names()[0:3:2]:
        info = ccsf_user.canvasProfile.get_assignment_objects(name, "upcoming")
        for new_assignment in info:
            if new_assignment["name"].lower() not in existing_assignments:
                assignment = {"class": name,
                              "date": new_assignment["due_at"],
                              "name": new_assignment["name"]}
                assignments_list.append(assignment)

    # Add to Notion
    ucdavis_user.postDatabase(assignments_list)




if __name__ == "__main__":
    main()
