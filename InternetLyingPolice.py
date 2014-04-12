import praw             # For reddit API
import sys              # Used for stderr message output
import ConfigParser     # Used to read config file (for authentication)

# Reading config file
config = ConfigParser.ConfigParser()
config.read('policebot.ini')

green_light = True      # Boolean later used to prevent duplicate comments
# From config file
username = config.get('Authentication', 'Username')
password = config.get('Authentication', 'Password')

user_agent = "InternetLyingPolice by /u/Antrikshy"
snarky_sarcasm = "INTERNET POLICE! GET DOWN ON THE GROUND! \
                \n\nAlleged liar please step forward with your hands \
                above your head! \
                \n\n---\
                \n\n^^Just ^^a ^^silly, ^^in-development ^^bot ^^by \
                ^^/u/Antrikshy."

# All the cool stuff happens here
def main():
    # r is the reddit object from now on
    r = praw.Reddit(user_agent)
    r.login(username, password)
    print >> sys.stderr, "Logged in."

    phrases_to_look_for = ("this never happened", "lie on the Internet",
                           "OP is lying", "Internet and tell lies",
                           "Just Go On the Internet and Tell Lies?",
                           "OP is a liar", "is a phony", "big fat phony",
                           "is a liar")

    # Neverending loop to run bot continuously
    while (True):
        print >> sys.stderr, "Initializing scanner..."
        police_scanner(r, phrases_to_look_for)

''' With a series of for-loops, this method reads comments from the 
    comment_stream and scans for phrases. For each fetched comment in a batch,
    the bot goes through all the phrases. If one is found, sarcasm is posted.
    The loops also check the usernames of everyone who has replied to each 
    comment. If this bot is one of them, the green_light is switched off and the
    comment will be ignored. '''
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
        print >> sys.stderr, comment_count
        # Scan for each phrase
        for phrase in phrases:
            green_light = True
            print >> sys.stderr, "Searching for phrases..."
            # If phrase found
            if phrase in scanning.body:
                # Check replies to see if already replied
                for reply in scanning.replies:
                    if reply.author.name == "InternetLyingPolice":
                        print >> sys.stderr, "Already replied."
                        green_light = False

                # If not already replied
                if (green_light):
                    print >> sys.stderr, "Something found!"
                    post_snarky_comment(scanning)

        # main() fetches more comments if this batch is done
        if comment_count == 1000:
            break

''' Method that simply replies to the comment passed in as parameter '''
''' Parameters:
    reply_to: Comment to reply to '''
def post_snarky_comment(reply_to):
    print >> sys.stderr, "Posting sarcasm..."
    reply_to.reply(snarky_sarcasm)

if __name__ == '__main__':
    main()