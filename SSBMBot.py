import json
import praw
import re
from time import sleep

reddit = praw.Reddit('bot1', user_agent='bot1 user agent')

subreddit = reddit.subreddit("SSBM")

replies = 0

print(reddit.user.me())

with open("words.json") as f:
    words = json.load(f)

with open("commented.txt", "r+") as log:
    while True:
        new_comments = (comment for comment in subreddit.comments(
            limit=1000) if comment.id not in log.read())

        for comment in new_comments:
            for word in words:
                if re.search("!{0}".format(word), comment.body, flags=re.IGNORECASE):
                    comment.reply("**{0}**\n\n{1}\n\n{2}\n\n{3}".format(
                        words[word]['name'],
                        "\n\n".join(words[word]['description']),
                        "\n\n".join("[{0}]({1})".format(link, words[word]['links'][link])
                                    for link in words[word]['links']),
                        "------\n[^SSBMBot](https://github.com/thearctickitten/SSBMBot) ^by ^[TheArcticKitten](/u/thearctickitten)---"
                    ))

                    # already_commented.append(comment)
                    log.write(comment.id + "\n")

                    replies += 1
                    print("Replied to comment ID:" + comment.id + " Count: " + replies)

    sleep(10)
