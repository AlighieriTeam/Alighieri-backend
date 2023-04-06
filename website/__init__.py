from typing import Optional

from flask import Flask, session
from flask_socketio import join_room, leave_room, send, SocketIO
from .room import Room

rooms = {}


def find_game(pin: str) -> Optional[Room]:
    return rooms.get(pin)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    @socketio.on("connect")
    def connect(auth):
        pass

    return app, socketio
