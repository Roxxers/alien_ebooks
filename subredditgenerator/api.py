import praw
import asyncio
import markovify
from pony.orm import db_session

from subredditgenerator import app, sub_api, models, markov
from subredditgenerator import mem_cache
from flask_restful import Resource, reqparse, abort
from flask import jsonify


reddit = praw.Reddit(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    user_agent=app.config["USER_AGENT"]
    )


parser = reqparse.RequestParser()


class SubredditEndpoint(Resource):
    @db_session
    def get(self, name):
        # Maybe allow multiple subreddits in future
        parser.add_argument('amount', default=1, type=int, help="Amount of markov-chain titles to return.")

        name = name.lower()
        args = parser.parse_args()
        subreddit = models.Subreddit.get(name=name)

        # If we can't find the subreddit in the db, return 404
        if not subreddit:
            abort(404, message="Subreddit not found in our database")
        else:
            gen = markov.MarkovGenerator(subreddit, mem_cache)
            sentences = gen.generate_sentences(args["amount"])
            return jsonify(sentences)


    
    #@db_session
    #def post(self, name):
    #    subreddit = reddit.subreddit(name)
    #    db_sub = models.Subreddit(name=subreddit.display_name.lower())
    #    for submission in subreddit.top(limit=None):
    #        models.Titles(id=int(submission.id, 36), title=submission.title, subreddit=db_sub)



sub_api.add_resource(SubredditEndpoint, '/api/v1/subreddit/<name>/markov')
