import json

import requests

courses = {"ECS03": "1bc57f41-8489-47f9-9dfa-f6bffc9ebbe1",
           "MAT021": "a937c8b2f7bd4c878e0a27dcd8896001",
           "ENG003": "e239745e2cb24cc087b75ff05384de18",
           "CLA010": "fe6f284c43b9428bb58274be424dd869",
           "FilmHistory": "3536d74f-067c-4df8-9b08-4ab83b5fe376",
           "IntroductiontoSociology": "3536d74f-067c-4df8-9b08-4ab83b5fe376",
           "OrientationLeaderSummerTraining": "3536d74f-067c-4df8-9b08-4ab83b5fe376",
           "PHY009": "90b1ce965ef248b8be983084826d0f1c",
           "MGT011": "f1ac21d02ca943a19d27c328a076cf80",
           "MAT021": "4924c2a0978c4f73956f821c290038ea",
           "BeyondtheBasics": "3536d74f-067c-4df8-9b08-4ab83b5fe376"}

class NotionApi:

    def __init__(
            self,
            notionToken=None,
            database_id=None,
            schoolAb=None,
    ):
        self.database_id = database_id
        self.notionToken = notionToken
        self.schoolAb = schoolAb
        self.notionHeaders = {
            "Authorization": "Bearer " + notionToken,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.payload = {"page_size": 20}


    def getDetailAssignments(self):
        existing = []
        response = requests.post(f"https://api.notion.com/v1/databases/{self.database_id}/query",
                                 headers=self.notionHeaders, json=self.payload)
        current_assignments = response.json()["results"]
        for assignment in current_assignments:
            if assignment["properties"]["Due date"]["date"] is not None:
                modified = {"name": assignment["properties"]["Name"]["title"][0]["text"]["content"],
                            "date": assignment["properties"]["Due date"]["date"]["start"]}
                existing.append(modified)
        return existing

    def getAssignments(self):
        existing = []
        response = requests.post(f"https://api.notion.com/v1/databases/{self.database_id}/query",
                                headers=self.notionHeaders, json=self.payload)
        current_assignments = response.json()["results"]
        for assignment in current_assignments:
            existing.append(assignment["properties"]["Name"]["title"][0]["text"]["content"].lower())
        return existing

    def addAssignments(self, assignments):
        for assignment in assignments:
            newPageData = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Status": {
                        "type": "status",
                        "status": {
                            "id": "e98f3afe-4456-4d0e-98c2-cde86a914a15",
                            "name": "Not started",
                            "color": "default"
                        }
                    },
                    "Complete": {
                        "type": "checkbox",
                        "checkbox": False
                    },
                    "Type": {
                        "type": "select",
                        "select": {
                            "id": "938cbacb-5c6c-4a22-a0e9-a6fd2201eac1",
                            "name": "Homework",
                            "color": "brown"
                        }
                    },
                    "Due date": {
                        "type": "date",
                        "date": {
                            "start": assignment["date"],
                            "time_zone": "America/Los_Angeles",
                        }
                    },
                    "Course": {
                        "type": "relation",
                        "relation": [{
                            "id": courses.get(assignment["class"], "3536d74f-067c-4df8-9b08-4ab83b5fe376")
                        }]
                    },
                    "Name": {
                        "type": "title",
                        "title": [
                            {
                                "type": "text",
                                "text": {
                                    "content": assignment["name"]
                                }
                            }
                        ]
                    }
                }
            }
            data = json.dumps(newPageData)
            response = requests.post(f"https://api.notion.com/v1/pages",
                                     headers=self.notionHeaders, data=data)
