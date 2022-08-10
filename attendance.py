import os
import random

import requests
from bs4 import BeautifulSoup as bs


def throw_coin():
    return random.choice([True, False])



def handler(event, context):
    if not all([throw_coin(), throw_coin()]):
        return

    LOGIN_INFO = {
        "mb_id": os.getenv("ATTENDANCE_ID", ""),
        "mb_password": os.getenv("ATTENDANCE_PW", ""),
    }
    LOGIN_URL = os.getenv("ATTENDANCE_LOGIN_URL", "")
    GET_POINT_URL = os.getenv("ATTENDANCE_GET_POINT_URL", "")
    POST_POINT_URL = os.getenv("ATTENDANCE_POST_POINT_URL", "")

    with requests.Session() as s:
        login_req = s.post(LOGIN_URL, data=LOGIN_INFO)
        print(login_req.status_code)

        attendance_page = s.get(GET_POINT_URL)
        soup = bs(attendance_page.text, "html.parser")
        soup.find()
        secdoe = soup.find("input", {"name": "secdoe"})
        proctype = soup.find("input", {"name": "proctype"})

        ATTENDANCE_INFO = {
            "secdoe": secdoe.get("value"),
            "proctype": proctype.get("value"),
        }
        attendance_req = s.post(
            POST_POINT_URL,
            data=ATTENDANCE_INFO,
        )

        print(attendance_req.status_code)
