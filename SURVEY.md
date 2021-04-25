# Survey in Profile-Readme

### Why i did this
I did this because I wanted to have some action in my Readme, so I did it!

## What you need

- **[Shlink](https://shlink.io)** _Shlink is an self-hosted URL-Shortener witth an REST-API_
- **A PHP-server** _(for shlink)_
- **A GitHub-Account** _(That should be clear)_


## Quick start
1. Get the update_readme.py, the requirements.txt and the questions-folder into your repo.
2. Create a new action from scratch with [this](https://github.com/mawoka-myblock/mawoka-myblock/blob/main/.github/workflows/survey.yml) content
3. Set some repo-secrets:
    - BASE_URL = The url for your shlink-instance with https (or http)
    - NO_RUL = The url-for the no-selection (if https://go.example.com/HiLp would be your short-url then it would be "HiLp")
    - YES_URL = the same as NO_URL, but for yes
    - SHLINK_API_KEY = the api-key for shlink
    - SHLINK_TAG = the tag you gave the yes- and no-urls

4. Edit the update_readme.py file at the bottom, where you have to place your readme.




# Known problems
- On year-change the script will do stuff, I didn't test and I don't even want to test... 🙈

