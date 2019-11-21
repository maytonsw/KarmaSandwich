import praw 
import logging

def searchSubmission(comments, candidates):     # Searches a submission for comments that fit the correct pattern

    logging.info('Starting submission search.')
    for comment in comments.list():             # comments is converted to a list to perform operations
        if not comment.is_root:                 # Checks if the comment's parent is a top-level comment
            parent = comment.parent()           
            logging.debug('Comment is not root')
            if not parent.is_root:              # Checks if the comment's grandparent is a top-level comment
                grandparent = parent.parent()
                logging.debug('Parent comment is not root.') #500       # 4                                        3
                if comment.score > 200 and comment.score > parent.score * 3 and grandparent.score > parent.score * 2:   # Compares the 3 comments, looking for a weighted A > B < C pattern
                    candidates.append('reddit.com' + comment.permalink + '?context=10000')                              # Builds a properly formatted permalink and appends it to the candidates list
                    logging.debug('New candidate comment found.')

def submitResults(candidates, r):            # Submits the permalinks of the qualifying comments to the /r/KarmaSandwich subreddit

    for candidate in candidates:
        try:                                                                              
            r.subreddit('KarmaSandwich').submit('Karma Sandwich', url=candidate, resubmit=False)     # Checks for duplicate submissions
        except praw.exceptions.APIException:
            logging.error('This sandwich has already been submitted!')
        logging.info('Submitted successfully.')