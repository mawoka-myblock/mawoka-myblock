import datetime
import json
import os

import jinja2
from flask import Flask, redirect, Response
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from jinja2 import Environment, select_autoescape
import requests
from deta import Deta

env = Environment(
    loader=jinja2.FileSystemLoader('./'),
    autoescape=True
)
deta = Deta()
db = deta.Base('get-liked-music')
google_data = {}
with open("client_secrets.json", "r") as f:
    google_data = json.load(f)["web"]
SCOPES = ['https://www.googleapis.com/auth/youtube']
refresh_token = os.getenv("REFRESH_TOKEN")
"""
flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)

flow.redirect_uri = "http://localhost"


authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    prompt='consent',
    # approval_prompt='force',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')

print(authorization_url)

flow.fetch_token(code="TOKEN")
print(flow.credentials.refresh_token)
"""

# print(creds.valid)
app = Flask(__name__)
api_service_name = "youtube"
api_version = "v3"


@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response


@app.route('/pic/<index>', methods=["GET"])
def hello_world(index: int):
    try:
        int(index)
    except ValueError:
        return "", 404
    if int(index) >= 5:
        return "", 404
    res = db.get(f"pic:{index}")
    if res is not None:
        print("Cached")
        return Response(res["value"], mimetype="image/svg+xml")
    creds = Credentials(refresh_token, refresh_token=refresh_token,
                        token_uri="https://accounts.google.com/o/oauth2/token",
                        client_id=google_data["client_id"], client_secret=google_data["client_secret"])
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
    rendered_template = template.render(data)
    db.put(rendered_template, f"pic:{index}", expire_at=datetime.datetime.now() + datetime.timedelta(hours=1))
    return Response(rendered_template, mimetype="image/svg+xml")


@app.route('/click/<index>', methods=["GET"])
def click(index: int):
    try:
        int(index)
    except ValueError:
        return "", 404
    if int(index) >= 5:
        return "", 404

    res = db.get(f"click:{index}")
    if res is not None:
        print("Cached")
        return redirect(
            res["value"],
            code=301)
    creds = Credentials(refresh_token, refresh_token=refresh_token,
                        token_uri="https://accounts.google.com/o/oauth2/token",
                        client_id=google_data["client_id"], client_secret=google_data["client_secret"])
    youtube = build(
        api_service_name, api_version, credentials=creds)
    vid_id = youtube.playlistItems().list(playlistId="LM", part="snippet").execute()
    vid_url = f'https://www.youtube.com/watch?v={vid_id["items"][int(index)]["snippet"]["resourceId"]["videoId"]}'
    db.put(vid_url, f"click:{index}", expire_at=datetime.datetime.now() + datetime.timedelta(hours=1))
    return redirect(
        vid_url,
        code=301)
