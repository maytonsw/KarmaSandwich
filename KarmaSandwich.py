# Written by Sean Mayton
# Python 3.6
# PRAW 5.4 -> 6.0
# Test

import praw         # Python wrapper for Reddit API
import sys
import pprint
import logging

from Operations import searchSubmission
from Operations import submitResults

# main  
candidates = []
title = 'Karma Sandwich'

logging.basicConfig(filename='sandwich.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)
logging.info('Program start.')

try:
    logging.info('Logging in.')
    r = praw.Reddit()      # Builds a Reddit instance using credentials stored in the local praw.ini file
    logging.info('Logged in successfully!')
except praw.exceptions.PRAWException as err:
    logging.error('API Exception on login:' + str(err) + '\nRecheck login credentials.')
    sys.exit(0)
                              
for submission in r.subreddit('askreddit+iama+funny+aww+pics+videos+showerthoughts+todayilearned').top('week'):     # 100 iterations
    logging.info(submission.title)                  
    submission.comment_sort = 'top'                 # Sets CommentForest to be sorted by top scores
    comments = submission.comments                  # Builds a Comments instance
    submission.comments.replace_more(limit=0)       # Clears the "load more comments" objects from the CommentForest
    searchSubmission(comments, candidates)  

logging.info(candidates)
submitResults(candidates, r)