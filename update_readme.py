import requests
import json
import random

yes_url = "NxVd8"
no_url = "HfH3s"

api_key = "306e9825-0170-4daa-951e-36d44f3af59a"

with open("questions/unasked_questions.json", "r") as f:
    ua_questions = json.load(f)
    print(ua_questions)


random_question = random.randint(0, len(ua_questions)-1)
print(ua_questions[random_question])


with open("questions/asked_questions.json", "r") as f:
    asked_questions = json.load(f)
    asked_questions.append(ua_questions[random_question])


print(asked_questions)


with open("questions/asked_questions.json", "w") as f:
    json.dump(asked_questions, f)


with open("questions/unasked_questions.json", "w") as f:
    del ua_questions[random_question]
    json.dump(ua_questions, f)
    print(ua_questions)

