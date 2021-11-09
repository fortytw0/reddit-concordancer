import praw
import os
import json
import pandas as pd

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


subreddit_submissions = reddit.subreddit("reddevils").top("day")
submission_dict = {}
comment_dict = {}

submission_csv = []
comment_csv = []


i = 0


for submission in subreddit_submissions:

    print("Working on the {} comment...\n\n".format(i+1))

    try : 
        submission_dict['submission_subreddit'] = submission.subreddit.name
        submission_dict['submission_title'] = submission.title
        submission_dict['submission_created_utc'] = submission.created_utc 
        submission_dict['submission_is_self'] = submission.is_self
        submission_dict['submission_num_comments'] = submission.num_comments
        submission_dict['submission_id'] = submission.id
        submission_dict['submission_author'] = submission.author.name
        submission_dict['submission_score'] = submission.score
        submission_dict['submission_upvote_ratio'] = submission.upvote_ratio

        submission_csv.append(submission_dict)
        # print(submission_dict)
        print('Parsing submission...')
    except Exception as e : 
        print('Looks like there was an error with the submission : {}'.format(e))
    submission_dict = {}


    
    try:
        comments_forest = submission.comments
        for comment in comments_forest:
            
                # comment.refresh()

                comment_dict['comment_type'] = 'primary'
                comment_dict['comment_body'] = comment.body
                comment_dict['comment_author'] = comment.author.name
                comment_dict['comment_created_utc'] = comment.created_utc
                comment_dict['comment_id'] = comment.id
                comment_dict['comment_score'] = comment.score
                comment_dict['comment_submission_id'] = comment.submission.id
                comment_dict['comment_submission_title'] = comment.submission.title
                comment_dict['comment_subreddit'] = comment.submission.subreddit.name

                comment_csv.append(comment_dict)
                # print(comment_dict)
                print('Parsing main comment...')

                for reply in comment.replies : 

                    
                        comment_dict['comment_type'] = 'secondary'
                        comment_dict['comment_body'] = reply.body
                        comment_dict['comment_author'] = reply.author.name
                        comment_dict['comment_created_utc'] = reply.created_utc
                        comment_dict['comment_id'] = reply.id
                        comment_dict['comment_score'] = reply.score
                        comment_dict['comment_submission_id'] = reply.submission.id
                        comment_dict['comment_submission_title'] = reply.submission.title
                        comment_dict['comment_subreddit'] = reply.submission.subreddit.name

                        comment_csv.append(comment_dict)
                        # print(comment_dict)
                        print('Parsing replies...')

    except Exception as e : 
        print('Looks like there was an error with the comments : {}'.format(e))
    comment_dict = {}

    if i%20==0: 
        with open('submission.json', 'w') as f:
            json.dump(submission_csv, f) 


        with open('comment.json', 'w') as f:
            json.dump(comment_csv, f)

        i += 1
    else : 
        i += 1



