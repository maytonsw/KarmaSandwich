# Written by Sean Mayton
# Python 3.6
# PRAW 5.4 -> 6.0

import praw         # Python wrapper for Reddit API
import sys
import pprint
import logging

def searchSubmission(comments):     # Searches a submission for comments that fit the correct pattern

    logging.info('Starting submission search.')
    for comment in comments.list():             # comments is converted to a list to perform operations
        if not comment.is_root:                 # Checks if the comment's parent is a top-level comment
            parent = comment.parent()           
            logging.debug('Comment is not root')
            if not parent.is_root:              # Checks if the comment's grandparent is a top-level comment
                grandparent = parent.parent()
                logging.debug('Parent comment is not root.')            # 4                                        3
                if comment.score > 500 and comment.score > parent.score * 3 and grandparent.score > parent.score * 2:   # Compares the 3 comments, looking for a weighted A > B < C pattern
                    candidates.append('reddit.com' + comment.permalink + '?context=10000')                              # Builds a properly formatted permalink and appends it to the candidates list
                    logging.debug('New candidate comment found.')

def submitResults():            # Submits the permalinks of the qualifying comments to the /r/KarmaSandwich subreddit

    for candidate in candidates:
        try:                                                                              
            r.subreddit('KarmaSandwich').submit(title, url=candidate, resubmit=False)     # Checks for duplicate submissions
        except praw.exceptions.APIException:
            logging.error('This sandwich has already been submitted!')
        logging.info('Submitted successfully.')

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

for submission in r.subreddit('askreddit+iama+funny+aww+pics+videos+showerthoughts').top('week'):     # 100 iterations
    logging.info(submission.title)                  
    submission.comment_sort = 'top'                 # Sets CommentForest to be sorted by top scores
    comments = submission.comments                  # Builds a Comments instance
    submission.comments.replace_more(limit=0)       # Clears the "load more comments" objects from the CommentForest
    searchSubmission(comments)  

logging.info(candidates)
submitResults()