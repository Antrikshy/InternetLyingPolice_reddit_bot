import praw
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('policebot.ini')

green_light = True
username = config.get('Authentication', 'Username')
password = config.get('Authentication', 'Password')

user_agent = "InternetLyingPolice by /u/Antrikshy"
snarky_sarcasm = "INTERNET POLICE! GET DOWN ON THE GROUND! \
                \n\nAlleged liar please step forward with your hands \
                above your head! \
                \n\n---\
                \n\n^^Just ^^a ^^silly, ^^in-development ^^bot ^^by \
                ^^/u/Antrikshy."

def main():
    r = praw.Reddit(user_agent)
    r.login(username, password)
    print >> sys.stderr, "Logged in."

    phrases_to_look_for = ("this never happened", "lie on the Internet",
                           "OP is lying", "Internet and tell lies",
                           "Just Go On the Internet and Tell Lies?",
                           "OP is a liar", "is a phony", "big fat phony",
                           "is a liar")

    while (True):
        print >> sys.stderr, "Initializing scanner..."
        police_scanner(r, phrases_to_look_for)

def police_scanner(session, phrases):
    print >> sys.stderr, "Fetching comments..."
    comments = praw.helpers.comment_stream(session, "all", 
                                                limit = None, verbosity = 0)
    comment_count = 0

    for scanning in comments:
        print >> sys.stderr, "Scanning comments..."
        comment_count += 1
        print >> sys.stderr, comment_count

        for phrase in phrases:
            green_light = True
            print >> sys.stderr, "Searching for phrases..."
            if phrase in scanning.body:
                for reply in scanning.replies:
                    if reply.author.name == "InternetLyingPolice":
                        print >> sys.stderr, "Already replied."
                        green_light = False

                if (green_light):
                    print >> sys.stderr, "Something found!"
                    post_snarky_comment(scanning)

        if comment_count == 1000:
            break

def post_snarky_comment(reply_to):
    print >> sys.stderr, "Posting sarcasm..."
    reply_to.reply(snarky_sarcasm)

if __name__ == '__main__':
    main()