import praw
import os
import json

with open('secrets.json', 'r') as f: 
    secrets = json.load(f)


client_id = secrets['client_id'] # os.environ.get("REDDIT_CLIENT_ID", "")
client_password = secrets['client_secret'] # os.environ.get("REDDIT_CLIENT_PASSWORD", "")
user_agent = secrets['user_agent']
refresh_token = secrets['refresh_token']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_password,
    user_agent=user_agent,
    refresh_token=refresh_token
    
)

print(reddit.user.me().name)

subreddit_submissions = reddit.subreddit("liverpoolfc").top("day")
print(subreddit_submissions)

for submission in subreddit_submissions:
    print(submission)
    print(submission.title)
    print(submission.created_utc)
    print(submission.is_self)
    print(submission.comments)
    print(submission.num_comments)
    print(submission.id)

