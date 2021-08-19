import praw
import os
import json
import requests

from urllib.parse import urlparse, parse_qs

with open('secrets.json', 'r') as f: 
    secrets = json.load(f)


client_id = secrets['client_id']
client_password = secrets['client_secret']
user_agent = secrets['user_agent']
redirect_uri = secrets['user_agent']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_password,
    user_agent=user_agent,
    redirect_uri=redirect_uri)

url_request = reddit.auth.url(["identity", "read"], "...", "permanent", implicit=False)



'''
TODO: Automatically handle this part of the code to get the URL from the redirect URI
'''


secrets['auth_url'] = input('Please enter authentication url-->')

secrets['auth_code'] = parse_qs(urlparse(secrets['auth_url']).query)['code']

secrets['refresh_token'] = reddit.auth.authorize(secrets['auth_code'])
secrets['auth_me'] = reddit.user.me().name


with open('secrets.json', 'w') as f : 
    json.dump(secrets, f)