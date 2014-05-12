import praw             # For reddit API
import sys              # Used for stderr message output
import time             # To make the bot sleep
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
                \n\n^^Just ^^a ^^silly, ^^in-development ^^bot ^^by \
                ^^/u/Antrikshy. \
                \n\n^^Currently, ^^it ^^may ^^not ^^run ^^24x7 ^^so \
                ^^don't ^^try ^^to ^^play ^^with ^^it."

# All the cool stuff happens here
def main():
    # r is the reddit object from now on
    r = praw.Reddit(USER_AGENT)
    r.login(USERNAME, PASSWORD)
    print >> sys.stderr, "Logged in."

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

    raise HTTPError
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
    try:
        print >> sys.stderr, "Posting sarcasm..."
        reply_to.reply(SNARKY_SARCASM)

    except urllib2.HTTPError as e:
        print >> sys.stderr, "Got HTTPError from reddit:" + e.code
        if e.code == 403:
            print >> sys.stderr, "Posting in restricted subreddit."
        print >> sys.stderr, "Nothing to see here. Moving on."

    except Exception as e:
        print >> sys.stderr, "Got some non-HTTPError exception."
    
if __name__ == '__main__':
    main()