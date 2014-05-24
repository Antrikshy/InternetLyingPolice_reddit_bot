# Copyright 2014, Antriksh Yadav

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import praw             # For reddit API
import sys              # Used for stderr message output
import time             # To make the bot sleep
import threading        # To run second thread that cleans up downvoted posts
import urllib2          # To except HTTPError
import ConfigParser     # Used to read config file (for authentication)

# Reading config file
config = ConfigParser.ConfigParser()
config.read('policebot.ini')

green_light = True      # Boolean later used to prevent duplicate comments
# From config file
USERNAME = config.get('Authentication', 'Username')
PASSWORD = config.get('Authentication', 'Password')

USER_AGENT = "InternetLyingPolice by /u/Antrikshy"
SNARKY_SARCASM = "Internet Police! Get down! \
                \n\nAlleged liar please step forward with your hands \
                above your head! \
                \n\n^^Just ^^a ^^silly ^^bot ^^by ^^/u/Antrikshy. \
                \n\n^^Comments ^^now ^^deleted ^^if ^^people ^^hate ^^them."

# All the cool stuff happens here
def main():
    # r is the reddit object from now on
    r = praw.Reddit(USER_AGENT)
    r.login(USERNAME, PASSWORD)
    print >> sys.stderr, "Logged in."

    # Old comment scanner-deleter to delete <1 point comments every half hour
    t = threading.Thread(target=delete_downvoted_posts, args=(r,))
    t.start()

    phrases_to_look_for = ("this never happened", "lie on the Internet",
                           "OP is lying", "Internet and tell lies",
                           "Just Go On the Internet and Tell Lies?",
                           "is a phony", "big fat phony", "are a liar",
                           "is a liar", "because it didn't happen", 
                           "they are lying", "he is lying", "she is lying")

    # Neverending loop to run bot continuously
    while (True):
        print >> sys.stderr, "Initializing scanner..."
        police_scanner(r, phrases_to_look_for)
        # Sleeps for 15 seconds (seems to fix repeat commenting for now)
        print >> sys.stderr, "Taking 15 second donut break..."
        time.sleep(15)
        print >> sys.stderr, "I'm full."

''' With a series of for-loops, this method reads comments from the 
    comment_stream and scans for phrases. For each fetched comment in a batch,
    the bot goes through all the phrases. If one is found, sarcasm is posted.
    The loops also check the usernames of everyone who has replied to each 
    comment. If this bot is one of them, the green_light is switched off and 
    the comment will be ignored. '''
''' Parameters:
    session: The reddit session to use
    phrases: Array of phrases to scan for '''

def police_scanner(session, phrases):
    print >> sys.stderr, "Fetching comments..."
    # comments now stores all the comments pulled using comment_stream
    # Change "all" to "subreddit-name" to scan a particular sub
    # limit = None fetches max possible comments (about 1000)
    # See PRAW documentation for verbosity explanation (it is not used here)
    comments = praw.helpers.comment_stream(session, "all", 
                                                limit = None, verbosity = 0)
    comment_count = 0   # Number of comments scanned (for stderr message)

    # Read each comment
    for scanning in comments:
        print >> sys.stderr, "Scanning comments..."
        comment_count += 1
        green_light = True
        print >> sys.stderr, comment_count
        # Scan for each phrase
        for phrase in phrases:
            print >> sys.stderr, "Searching for phrases..."
            # If phrase found
            if phrase in scanning.body:
                # Check replies to see if already replied
                for reply in scanning.replies:
                    if reply.author.name == "InternetLyingPolice":
                        print >> sys.stderr, "Already replied."
                        green_light = False
                        break

                # If not already replied
                if (green_light == True):
                    print >> sys.stderr, "Something found!"
                    post_snarky_comment(scanning)
                    print >> sys.stderr, "Posted sarcasm."
                    break

        # main() fetches more comments if this batch is done
        # comment_stream seems to grab more than 1000 comments. I limited
        # each batch to 1000 manually to keep things manageable in case I 
        # expand
        if comment_count == 1000:
            return;

''' Method that simply replies to the comment passed in as parameter '''
''' Parameters:
    reply_to: Comment to reply to '''
def post_snarky_comment(reply_to):
    # Post comment
    try:
        print >> sys.stderr, "Posting sarcasm..."
        reply_to.reply(SNARKY_SARCASM)

    # If reddit returns error (when bot tries to post in unauthorized sub)
    except urllib2.HTTPError as e:
        print >> sys.stderr, "Got HTTPError from reddit:" + e.code
        if e.code == 403:
            print >> sys.stderr, "Posting in restricted subreddit."
        print >> sys.stderr, "Nothing to see here. Moving on."

    # To catch any other exception
    except Exception as e:
        print >> sys.stderr, "Got some non-HTTPError exception."

''' Method to delete old comments that have been downvoted. Scans last 25 
    comments every half hour. '''
''' Parameters:
    session: The reddit session to use '''
def delete_downvoted_posts(session):
    while (True):
        print >> sys.stderr, "\n" + "Starting old comments scanner."
        # Get own account
        my_account = session.get_redditor(USERNAME)
        # Get last 25 comments
        my_comments = my_account.get_comments(limit = 10)

        # Delete all comments with <1 point
        for old_comment in my_comments:
            if old_comment.score <= 0:
                print >> sys.stderr, "Found failed joke, deleting."
                old_comment.delete()

        # Sleep for half hour
        print >> sys.stderr, "Turning down old comment scanner for 30 mins..."
        time.sleep(1800)

if __name__ == '__main__':
    main()