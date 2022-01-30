import json
import os

import jinja2
from flask import Flask, redirect, Response
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from jinja2 import Environment, select_autoescape
import requests

env = Environment(
    loader=jinja2.FileSystemLoader('./'),
    autoescape=True
)
google_data = {}
with open("client_secrets.json", "r") as f:
    google_data = json.load(f)["web"]
SCOPES = ['https://www.googleapis.com/auth/youtube']

# flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
#
# flow.redirect_uri = "http://localhost"


# authorization_url, state = flow.authorization_url(
#     # Enable offline access so that you can refresh an access token without
#     # re-prompting the user for permission. Recommended for web server apps.
#     access_type='offline',
#     prompt='consent',google_data
#     # approval_prompt='force',
#     # Enable incremental authorization. Recommended as a best practice.
#     include_granted_scopes='true')

refresh_token = os.getenv("REFRESH_TOKEN")
# flow.fetch_token(code=code)


# print(creds.valid)
app = Flask(__name__)
api_service_name = "youtube"
api_version = "v3"


@app.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    return response


@app.route('/pic/<index>', methods=["GET"])
def hello_world(index: int):
    try:
        int(index)
    except ValueError:
        return "", 404
    if int(index) >= 5:
        return "", 404
    creds = Credentials(refresh_token, refresh_token=refresh_token,
                        token_uri="https://accounts.google.com/o/oauth2/token",
                        client_id=google_data["client_id"], client_secret=google_data["client_secret"])
    print(creds.valid)
    youtube = build(
        api_service_name, api_version, credentials=creds)
    vid_id = youtube.playlistItems().list(playlistId="LM", part="snippet").execute()
    # print(json.dumps(vid_id["items"][0]["snippet"]))
    thumbnail_url = vid_id["items"][int(index)]["snippet"]["thumbnails"]["default"]["url"]
    req = requests.get(thumbnail_url)
    # print(thumbnail_url)
    data = {
        "title": vid_id["items"][int(index)]["snippet"]["title"],
        "artist": vid_id["items"][int(index)]["snippet"]["videoOwnerChannelTitle"],
        "thumbnail": f"data:image/jpeg;base64,{base64.b64encode(req.content).decode('utf-8')}",
        "url": f'https://www.youtube.com/watch?v={vid_id["items"][int(index)]["snippet"]["resourceId"]["videoId"]}'
    }
    template = env.get_template("svg_template.jinja2")
    return Response(template.render(data), mimetype="image/svg+xml")


@app.route('/click/<index>', methods=["GET"])
def click(index: int):
    try:
        int(index)
    except ValueError:
        return "", 404
    if int(index) >= 5:
        return "", 404
    creds = Credentials(refresh_token, refresh_token=refresh_token,
                        token_uri="https://accounts.google.com/o/oauth2/token",
                        client_id=google_data["client_id"], client_secret=google_data["client_secret"])
    print(creds.valid)
    youtube = build(
        api_service_name, api_version, credentials=creds)
    vid_id = youtube.playlistItems().list(playlistId="LM", part="snippet").execute()
    return redirect(
        f'https://www.youtube.com/watch?v={vid_id["items"][int(index)]["snippet"]["resourceId"]["videoId"]}',
        code=301)
