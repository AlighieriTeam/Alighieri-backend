import json
from typing import Optional

from flask import Flask, session
from flask_socketio import join_room, leave_room, send, SocketIO, emit
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
    def connect():
        room = session.get("room")
        player = json.loads(session.get("player"))
        if not room or not player:
            return
        if room not in rooms:
            leave_room(room)
            return

        join_room(room)

        emit("connection", player, to=room)
        print(f"{player['name']} joined room {room}")

    return app, socketio
