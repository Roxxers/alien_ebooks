import time
import logging
import sys

from celery import current_app
from flask import request

from alien_ebooks import socketio, celery


def emit_build_update(task, room):
    data = {
        "state": task.state,
        "current": task.info.get("current"),
        "total": task.info.get("total"),
        "status": task.info.get("status", ""),
        "subreddit": task.info.get("subreddit", "")
    }
    socketio.emit("build_update", data, json=True, room=room)


@socketio.on("build_request")
def handle_build_request(json):
    finished = False
    room = request.sid
    task = celery.add_titles_to_db.AsyncResult(json["buildID"])

    if not task.info:
        socketio.send("Build request doesn't exist", room=room)
    else:
        # Task does exist
        while task.status != "FINISHED":
            # Check on task every half second
            emit_build_update(task, room)
            time.sleep(0.5)
        # One last emit to make sure client knows generation is finished.
        emit_build_update(task, room)
