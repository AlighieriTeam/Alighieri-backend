# to kill process on web port 5000 in linux: fuser -k 5000/tcp
from flask import session
from flask_socketio import emit, join_room

from website import create_app

app, socketio = create_app()


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
