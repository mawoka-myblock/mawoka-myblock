import json
import random
import datetime
import urllib3
import os


http = urllib3.PoolManager()

yes_url = os.environ.get("YES_URL", "")
no_url = os.environ.get("NO_URL", "")

shlink_tag = os.environ.get("SHLINK_TAG", "")
base_url = os.environ.get("BASE_URL", "")
api_key = os.environ.get("SHLINK_API_KEY", "")

with open("questions/unasked_questions.json", "r") as f:
    ua_questions = json.load(f)


random_question = random.randint(0, len(ua_questions)-1)


with open("questions/asked_questions.json", "r") as f:
    asked_questions = json.load(f)
    asked_questions.append(ua_questions[random_question])


def last_qeustion():
    with open("questions/last_week.txt", "r") as f:
        return f.read()


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

yes_percent = int(json.loads(getstats("yes", "last"))["visits"]["pagination"]["totalItems"]) / int(json.loads(getplayers("last"))["visits"]["pagination"]["totalItems"])
no_percent = int(json.loads(getstats("no", "last"))["visits"]["pagination"]["totalItems"]) / int(json.loads(getplayers("last"))["visits"]["pagination"]["totalItems"])
print(int(round(no_percent, 2) * 100))
print(int(round(yes_percent, 2) * 100))


readme = f"""


<!--

<p align="center">

<img src="https://github.com/mawoka-myblock/mawoka-myblock/raw/main/intro.gif" />

</p>

-->
# Question

## {ua_questions[random_question]}

[![](https://img.shields.io/badge/-Yes-brightgreen?style=for-the-badge)](https://go.mawoka.eu.org/NxVd8) [![](https://img.shields.io/badge/-No-red?style=for-the-badge)](https://go.mawoka.eu.org/HfH3s)

Results are published every Sunday at 2:00AM

## Results from last week

### For the following question: {last_qeustion()}

|Yes/No |Percent|

|-------|-------|

|**Yes**| {int(round(yes_percent, 2) * 100)}|

|**No** | {int(round(no_percent, 2) * 100)}|

## My "Skills":

- <img src="https://simpleicons.org/icons/python.svg" height="17em" align="center" alt="Python" title="Python"/> **Python**
- <img src="https://simpleicons.org/icons/java.svg" height="17em" align="center" alt="Java" title="Java"/> **Java**
- <img src="https://simpleicons.org/icons/javascript.svg" height="17em" align="center" alt="JavaScript" title="JavaScript"/> **JavaScript**
- <img src="https://simpleicons.org/icons/mongodb.svg" height="17em" align="center" alt="MongoDB" title="MongoDB"/> **MongoDB**

---
- <img src="https://simpleicons.org/icons/linux.svg" height="30em" align="center" alt="Linux" title="Linux"/> **Linux:**

	- Systemadministration

	- I'm using Manjaro [<img src="https://manjaro.org/img/logo.svg" height="15em" align="center" alt="Manjaro" title="Manjaro"/>](https://manjaro.org) with KDE [<img src="https://kde.org/media/images/trademark_kde_gear_black_logo.png" height="15em" align="center" alt="KDE" title="KDE"/>](https://kde.org) Plasma [<img src="https://kde.org/images/plasma.svg" height="15em" align="center" alt="Plasma" title="Plasma"/>](https://kde.org/plasma-desktop)

	- On my servers I am using Debian [<img src="https://www.debian.org/logos/openlogo-nd.svg" height="15em" align="center" alt="Debian" title="Debian"/>](https://debian.org)
<!--
## Other stuff:

- **Privacy:**

- It isn't really a skill, but it is something I really like 💓


- **Tools I use regularly:**

- Android [<img src="https://simpleicons.org/icons/android.svg" height="20em" align="center" alt="Android" title="Android"/>](https://www.android.com/)

- PyCharm [<img src="https://simpleicons.org/icons/pycharm.svg" height="20em" align="center" alt="PyCharm" title="PyCharm"/>](https://www.jetbrains.com/pycharm/)

- Vikunja [<img src="https://kolaente.dev/vikunja/frontend/raw/branch/main/public/favicon.ico" height="20em" align="center" alt="Vikunja" title="Vikunja"/>](https://vikunja.io)
-->

[![Visits Badge](https://badges.pufler.dev/visits/mawoka-myblock/mawoka-myblock)](https://mawoka.eu.org/lol.html)

## Stats:

<!--START_SECTION:waka-->

```text

Week: 17 April, 2021 - 24 April, 2021

Other Stuff 3 hrs 2 mins ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀ 58.21 %

HTML 1 hrs 3 mins ⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀ 20.03 %

Python 0 hrs 47 mins ⣿⣿⣿⣶⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀ 14.87 %

JSON 0 hrs 6 mins ⣦⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀ 01.77 %

Vue 0 hrs 3 mins ⣤⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀ 01.08 %

```

<!--END_SECTION:waka-->

> Note: If there is a language, it doesn't mean that I am good at this language!

## Social-Stuff:

[![Mastodon Follow](https://img.shields.io/mastodon/follow/000197929?domain=https%3A%2F%2Fmastodon.online&style=social)](https://mastodon.online/invite/Mhw5dbRx)




"""

with open("questions/last_week.txt", "w") as f:
    f.write(ua_questions[random_question])


with open("questions/asked_questions.json", "w") as f:
    json.dump(asked_questions, f)


with open("questions/unasked_questions.json", "w") as f:
    del ua_questions[random_question]
    json.dump(ua_questions, f)


with open("README.md", "w") as f:
    f.write(readme)
