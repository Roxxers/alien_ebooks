import praw
import markovify
from pony.orm import db_session

from subredditgenerator import app, sub_api, models
from flask_restful import Resource, reqparse
from flask import jsonify


reddit = praw.Reddit(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    user_agent=app.config["USER_AGENT"]
    )


parser = reqparse.RequestParser()
parser.add_argument('amount', default=0, type=int, help="Amount of markov-chain titles to return.")


class SubredditEndpoint(Resource):
    # TODO: Pls fix me in later use so I can be used properly when I need to request a new sub for the db
    @db_session
    def get(self, name):
        name = name.lower()
        args = parser.parse_args()
        subreddits = []

        for name in name.split("+"):
            subreddits.append(reddit.subreddit(name))


        for subreddit in subreddits:
            if not models.Subreddit.get(id=int(subreddit.id, 36)):
                db_sub = models.Subreddit(id=int(subreddit.id, 36), name=subreddit.display_name.lower())
                for submission in subreddit.top(limit=None):
                    models.Titles(id=int(submission.id, 36), title=submission.title, subreddit=db_sub)

        titles = ""
        for subreddit in subreddits:
            for post in models.Subreddit.get(id=int(subreddit.id, 36)).titles:
                titles += f"{post.title}\n"

        text_chain = markovify.NewlineText(titles, well_formed=False, state_size=2)
        gen_sent = []

        # Only allow a max of 20 to be generated
        num_gen = args["amount"] if args["amount"] <= 20 else 20
        for _ in range(num_gen):
            gen_sent.append(text_chain.make_sentence())
        return jsonify(gen_sent)



sub_api.add_resource(SubredditEndpoint, '/api/subreddit/<name>')
