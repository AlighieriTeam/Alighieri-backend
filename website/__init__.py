from typing import Optional

from flask import Flask, session, url_for
from flask_socketio import SocketIO

from .room import Room, Player

rooms = {}

def find_game(pin: str) -> Optional[Room]:
    return rooms.get(pin)

def del_room(pin: str) -> None:
    if pin in rooms.keys():
        del rooms[pin]

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)


    from .views import views
    from .event_handlers.room_events import register_room_events
    from .event_handlers.game_events import register_game_events

    register_room_events(app, socketio)
    register_game_events(socketio)

    app.register_blueprint(views, url_prefix='/')

    return app, socketio
