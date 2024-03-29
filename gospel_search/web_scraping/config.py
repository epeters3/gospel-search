import os

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

CHURCH_ROOT_URL = "https://www.churchofjesuschrist.org"
ALL_CONFERENCES_URL = CHURCH_ROOT_URL + "/study/general-conference"
SCRIPTURES_ROOT_URL = CHURCH_ROOT_URL + "/study/scriptures"
RELATED_CONTENT_QUERY = 'footer[class*="study-notes"]'
BODY_QUERY = {"name": "div", "class": "body-block"}
