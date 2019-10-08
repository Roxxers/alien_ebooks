from flask_restful import Api, Resource, reqparse
from pony.orm import db_session, select
from prawcore import exceptions

from alien_ebooks import app, cache, celery, markov, models, reddit

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
        parser.add_argument("amount", default=1, type=int, help="Amount of markov-chain titles to return.")

        name = name.lower()
        args = parser.parse_args()
        subreddit = models.Subreddit.get(name=name)

        if not subreddit:
            # If we can"t find the subreddit in the db, return 404
            return self.default_404_response("Subreddit not found in our database")

        # Found subreddit in db, created sentences from a markov chain
        gen = markov.MarkovGenerator(subreddit, cache)
        sentences = gen.generate_sentences(args["amount"])
        message = "Generated titles successfully"
        return self.response(200, message=message, data=sentences)


class SubredditEndpoint(SubredditResource):
    def get(self, name):
        name = name.lower()
        with db_session:
            subreddit = models.Subreddit.get(name=name)

        if not subreddit:
            return self.default_404_response("Subreddit not found in our database")

        data = {
            "name": subreddit.name,
            "number_of_titles": len(subreddit.titles)
        }
        return self.response(200, data=data)

    def post(self, name):
        name = name.lower()
        # TODO: Add check to see if subreddit already exists

        try:
            subreddit = reddit.subreddit(name)
            # This line does nothing but try and bait the exception out so we can return a 404 if it is not a real subreddit
            _ = subreddit.subscribers

            task = celery.add_titles_to_db.delay(name)
            data = {
                "task_id": task.id
            }
            return self.response(202, message=f"Created build task successfully for subreddit {name}", data=data)
        except exceptions.PrawcoreException:
            # Subreddit is not found
            return self.default_404_response("Subreddit doesn't exist")


class AllSubredditsEndpoint(SubredditResource):
    def get(self):
        with db_session:
            subreddits = select(s for s in models.Subreddit)[:]
        data = [x.name for x in subreddits]
        return self.response(200, data=data)


class BuildTaskEndpoint(SubredditResource):
    def get(self, task_id):
        # Get task from queue
        task = celery.add_titles_to_db.AsyncResult(task_id)

        if not task.info:  
            # If task does not exist
            return self.default_404_response("Could not find task with that ID")

        if task.state == "PENDING":
            # job did not start yet
            data = {
                "state": task.state,
                "current": task.info.get("current"),
                "total": task.info.get("total"),
                "status": "Pending..."
            }
        elif task.state != "FAILURE":
            data = {
                "state": task.state,
                "current": task.info.get("current"),
                "total": task.info.get("total"),
                "status": task.info.get("status", "")
            }
        else:
            # something went wrong in the background job
            data = {
                "state": task.state,
                "status": str(task.info),  # this is the exception raised
            }
            return self.response(500, message="Task has failed.", data=data)
        return self.response(200, data=data)


API_BASE = "/api/v1"

api.add_resource(AllSubredditsEndpoint, f"{API_BASE}/subreddits/")
api.add_resource(SubredditEndpoint, f"{API_BASE}/subreddits/<name>")
api.add_resource(SubredditMarkovEndpoint, f"{API_BASE}/subreddits/<name>/markov")
api.add_resource(BuildTaskEndpoint, f"{API_BASE}/tasks/<task_id>")
