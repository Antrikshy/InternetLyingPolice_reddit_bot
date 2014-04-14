/u/InternetLyingPolice
======================
This is my first reddit bot. **I created it to learn Python, PRAW and using APIs in general.**

**I have tried to document it so that it is easy for beginners to understand. I'm hoping that this code will be helpful to anyone learning to write their own first bot.**

This is a simple example of a bot that scans all reddit comments as they come in. It looks for certain phrases in a comment (explained in the section "What it does") and makes a sarcastic reply.

Because this bot is built using PRAW (Python Reddit API Wrapper), it follows reddit's API guidelines automatically, not making too many API requests etc.

What it does
------------
Sometimes on reddit, OP (Original Poster) is suspected of lying in their post. We see comments like "this never happened" or "OP is a big fat phony" or something like "would someone just go on the Internet and tell lies". These comments are references to popular TV shows like *Family Guy* and *Arthur*.

This bot scans for certain key phrases that suggest one of these references has been made and jumps into that thread, screaming that the Internet Police as arrived and the alleged liar should show themselves with their hands up.

It's a fun little project I did, and it might not be perfect because I'm only getting my feet wet. **I would highly appreciate any improvements and pull requests.**

How it works
------------
This bot makes use of PRAW's comment_stream to continuously pull 1000 newest comments over and over in a forever loop. It scans each one using the list phrases_to_look_for. It runs until the program is interrupted manually.

The bot's authentication details (username/password) for login are stored in a very simple config file which I have not included in this repository. However, there's a description of how that works in the section "What you can do with this code".

What you can do with this code
------------------------------
**You can feel free to fork this code, use it in your own bot, or whatever else you want to do with it.**

Because this bot is open-source, I have not included the username and password for the reddit account in the code. Instead I put it into a .ini file which the bot reads when logging in.

If you were to run this bot on your computer, here's what you would do:
- **Install PRAW** (along with Python, of course) because my bot needs its features to run.
- Edit the policebot.ini.dist and rename it to remove the .dist. Add a reddit username and password in the placeholders.
- **Make changes on line 4** of InternetLyingPolice to point to the address of your .ini file.
- Run the bot using this command from the directory you put it into:
    python InternetLyingPolice.py

Of course you shouldn't run this exact code from your computer without making any changes or we'll end up with two reddit bots doing the exact same thing and people will hate both of them.

**Ways to help me out:**
- **[High priority]** The bot may sometimes comments twice (maybe when it looks at the same comment twice; stderr suggests that it scans the same batch over and over at times). Try to look for any logic problems with the green_light boolean. For now, repeat commenting is prevented by making the bot sleep for 15 seconds, which may also cause it to miss comments.
- Make efficiency improvements in this program (I'm almost certain it looks at some comments twice because it doesn't sleep).
- Add more common phrases to look for.
- Maybe add a way to make the bot *not* comment when someone says "not saying OP is lying, but..."