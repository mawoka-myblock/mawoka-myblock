import requests
import json
import random
import datetime
from icecream import ic
import urllib3


http = urllib3.PoolManager()

yes_url = "NxVd8"
no_url = "HfH3s"

shlink_tag = "readme"
base_url = "https://go.mawoka.eu.org"
api_key = ""

with open("questions/unasked_questions.json", "r") as f:
    ua_questions = json.load(f)


random_question = random.randint(0, len(ua_questions)-1)


with open("questions/asked_questions.json", "r") as f:
    asked_questions = json.load(f)
    asked_questions.append(ua_questions[random_question])


with open("questions/asked_questions.json", "w") as f:
    json.dump(asked_questions, f)


with open("questions/unasked_questions.json", "w") as f:
    del ua_questions[random_question]
    json.dump(ua_questions, f)


global header, params
headers = {'accept': 'application/json', 'X-Api-Key': api_key}
params = (('startDate', '2021-W16'), ('endDate', '2021-W16'))


def getstats(yes_no, week):
    global year, cweek
    year = datetime.datetime.now().date().strftime("%Y")
    cweek = datetime.datetime.today().strftime("%U")

    if week == "last":
        if yes_no == "yes":
            r = http.request('GET', f'{base_url}/rest/v2/short-urls/{yes_url}/visits?startDate={year}-W{int(cweek)-1}',
                             headers=headers)
            return r.data
        elif yes_no == "no":
            r = http.request('GET', f'{base_url}/rest/v2/short-urls/{no_url}/visits?startDate={year}-W{int(cweek)-1}',
                             headers=headers)
            return r.data
        else:
            return "Error"
    elif week == "this":
        if yes_no == "yes":
            r = http.request('GET', f'{base_url}/rest/v2/short-urls/{yes_url}/visits?startDate={year}-W{int(cweek)}',
                             headers=headers)
            return r.data
        elif yes_no == "no":
            r = http.request('GET', f'{base_url}/rest/v2/short-urls/{no_url}/visits?startDate={year}-W{int(cweek)}',
                             headers=headers)
            return r.data
        else:
            return "Error"
    else:
        return "Error"

def getplayers(week):
    if week == "this":
        r = http.request('GET', f"{base_url}/rest/v2/tags/{shlink_tag}/visits?startDate={year}-W{int(cweek)}", headers=headers)
        return r.data
    elif week == "last":
        r = http.request('GET', f"{base_url}/rest/v2/tags/{shlink_tag}/visits?startDate={year}-W{int(cweek)-1}", headers=headers)
        return r.data
    else:
        return "Error"


answer = json.loads(getstats("no", "last"))
print(answer["visits"]["pagination"]["totalItems"])


print(json.loads(getstats("no", "last"))["visits"]["pagination"]["totalItems"], "answered no and", json.loads(getstats("yes", "last"))["visits"]["pagination"]["totalItems"], "from", json.loads(getplayers("last"))["visits"]["pagination"]["totalItems"], "answered yes")
