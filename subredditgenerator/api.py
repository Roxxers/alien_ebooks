import praw
import asyncio
import markovify
from pony.orm import db_session

from subredditgenerator import app, sub_api, models, markov, celery
from subredditgenerator import mem_cache
from flask_restful import Resource, reqparse, abort
from flask import jsonify


reddit = praw.Reddit(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    user_agent=app.config["USER_AGENT"]
    )


parser = reqparse.RequestParser()


base_response = {
    "response_code": 0,
    "message": "",
    "data": {},
}


# TODO: Need to rework the endpoint results to be better designed json

class SubredditMarkovEndpoint(Resource):
    @db_session
    def get(self, name):
        # Maybe allow multiple subreddits in future
        parser.add_argument('amount', default=1, type=int, help="Amount of markov-chain titles to return.")
        
        # Copy base response to edit it localled
        response = base_response.copy()

        name = name.lower()
        args = parser.parse_args()
        subreddit = models.Subreddit.get(name=name)

        # If we can't find the subreddit in the db, return 404
        if not subreddit:
            response_code = 404
            response["response_code"] = response_code
            response["message"] = "Subreddit not found in our database"
            response["data"] = None
            return response, response_code
        else:
            # Found subreddit in db, created sentences from a markov chain
            gen = markov.MarkovGenerator(subreddit, mem_cache)
            sentences = gen.generate_sentences(args["amount"])
            
            response_code = 200
            
            response["response_code"] = response_code
            response["message"] = "Generated titles successfully"
            response["data"] = sentences
            
            return response, response_code


class SubredditBuildEndpoint(Resource):
    def get(self, name):
        pass


class SubredditEndpoint(Resource):
    def get(self, name):
        pass
    
    def post(self, name):
        task = celery.add_titles_to_db.delay(name)
        print(task.status)
        return task.status, 202


class SubredditsEndpoint(Resource):
    def get(self):
        pass
    
    
api_base = "/api/v1/"

sub_api.add_resource(SubredditEndpoint, f"{api_base}subreddit/<name>")
sub_api.add_resource(SubredditMarkovEndpoint, f"{api_base}subreddit/<name>/markov")
sub_api.add_resource(SubredditBuildEndpoint, f"{api_base}subreddit/<name>/progress")
