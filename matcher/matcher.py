import requests
import dotenv
import os
import smtplib
import ssl
from rich import print  # fnacy output

dotenv.load_dotenv()
API_HOST = os.environ.get("API_HOST")
API_KEY = os.environ.get("API_KEY")
HEADERS = {"api_key": API_KEY}
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL = os.environ.get("EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

port = 587


def emailer(match1, match2):
    # create safe ssl context
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(EMAIL_HOST, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(EMAIL, EMAIL_PASSWORD)
        message_1 = f"""
        Subject: R/teenagers match up
        This is automated message
        You have been matched up with {match1["username"]},
        good luck and stay safe. We cannot verify users be careful of people who might not be who they say they are
        regards
        Nullrequest aka u/helldogog
        """
        message_2 = f"""
        Subject: R/teenagers match up
        This is automated message
        You have been matched up with {match2["username"]},
        good luck and stay safe. We cannot verify users be careful of people who might not be who they say they are
        regards
        Nullrequest aka u/helldogog
        """
        server.sendmail(EMAIL, match2["email"], message_1)
        server.sendmail(EMAIL, match1["email"], message_2)
        server.quit()
    except Exception as e:
        print(e)
        print(match1, "\n", match2)


response = requests.get(f"{API_HOST}/api/all", headers=HEADERS)
if response.status_code != 200:
    print("the api seems to be broken FIX IT")
    print(response.status_code)
else:
    json = response.json()[
        "persons"
    ]  # grab a dict from json and pull out a python array of people
    for person in json:
        best_match = None
        best_match_percent = 0
        for matchs in json:
            if person["id"] == matchs["id"]:
                pass
            else:
                score = 0
                if best_match == None:
                    best_match = matchs
                    if person["hobby"] == matchs["hobby"]:
                        score += 1
                    if person["outdoor"] == matchs["outdoor"]:
                        score += 1
                    if person["sub_cult"] == matchs["sub_cult"]:
                        score += 1
                    best_match_percent = (score / 3) * 100
                else:
                    best_match = matchs
                    if person["hobby"] == matchs["hobby"]:
                        score += 1
                    if person["outdoor"] == matchs["outdoor"]:
                        score += 1
                    if person["sub_cult"] == matchs["sub_cult"]:
                        score += 1
                    match_percent = (score / 3) * 100
                    if match_percent > best_match_percent:
                        best_match = matchs
                        best_match_percent = match_percent
        emailer(best_match, person)
        # remove the matches from the array
        json.pop(json.index(best_match))
        json.pop(json.index(person))