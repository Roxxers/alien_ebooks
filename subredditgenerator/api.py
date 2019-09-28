import asyncio

import markovify
import praw
from flask import jsonify
from flask_restful import Api, Resource, abort, reqparse
from pony.orm import db_session, select
from prawcore import exceptions

from subredditgenerator import app, cache, celery, markov, models, reddit

api = Api(app)


class SubredditResource(Resource):
    def __init__(self):
        self.base_response = {
            "response_code": 0,
            "message": "",
            "data": {},
        }
        super().__init__()
    
    def response(self, response_code, message="", data=None):
        response = self.base_response.copy()
        response["response_code"] = response_code
        response["message"] = message
        response["data"] = data
        return response, response_code
    
    def default_404_response(self, message):
        return self.response(404, message=message)
        

class SubredditMarkovEndpoint(SubredditResource):
    @db_session
    def get(self, name):
        # Maybe allow multiple subreddits in future
        parser = reqparse.RequestParser()
        parser.add_argument('amount', default=1, type=int, help="Amount of markov-chain titles to return.")

        name = name.lower()
        args = parser.parse_args()
        subreddit = models.Subreddit.get(name=name)

        if subreddit:
            # Found subreddit in db, created sentences from a markov chain
            gen = markov.MarkovGenerator(subreddit, cache)
            sentences = gen.generate_sentences(args["amount"])
            message = "Generated titles successfully"
            
            return self.response(200, message=message, data=sentences)
        else:
            # If we can't find the subreddit in the db, return 404
            return self.default_404_response("Subreddit not found in our database")


class SubredditEndpoint(SubredditResource):
    def get(self, name):
        name = name.lower()
        with db_session:
            subreddit = models.Subreddit.get(name=name)
        
        if subreddit:
            data = {
                "name": subreddit.name,
                "number_of_titles": len(subreddit.titles)
            }
            return self.response(200, data=data)
        else:
            return self.default_404_response("Subreddit not found in our database")
            
    def post(self, name):
        name = name.lower()
        
        try:
            subreddit = reddit.subreddit(name)
            _ = subreddit.subscribers  # This line does nothing but try and bait the exception out so we can return a 404 if it is not a real subreddit
            
            task = celery.add_titles_to_db.delay(name)
            # TODO: This needs to be finished, basically figure out an endpoint for progress
            print(task.status)
            return task.status, 202
        except exceptions.PrawcoreException:
            # Subreddit is not found
            return self.default_404_response("Subreddit doesn't exist")
            

class AllSubredditsEndpoint(SubredditResource):
    def get(self):
        with db_session:
            subreddits = select(s for s in models.Subreddit)[:]
        data = [x.name for x in subreddits]
        return self.response(200, data=data)


class SubredditBuildEndpoint(SubredditResource):
    def get(self, name):
        pass
    
    
api_base = "/api/v1"

api.add_resource(AllSubredditsEndpoint, f"{api_base}/subreddits/")
api.add_resource(SubredditEndpoint, f"{api_base}/subreddits/<name>")
api.add_resource(SubredditMarkovEndpoint, f"{api_base}/subreddits/<name>/markov")
