import json
from typing import Optional

from flask import Flask, session
from flask_socketio import join_room, leave_room, send, SocketIO, emit
from .room import Room

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

    app.register_blueprint(views, url_prefix='/')

    @socketio.on("connected")
    def connected():
        room = session.get("room")
        player = json.loads(session.get("player"))
        if not room or not player:
            return
        if room not in rooms:
            leave_room(room)
            return

        join_room(room)
        curr_game = find_game(room)
        if player not in curr_game.get_player_dict_list():
            player = curr_game.add_player()
            player = vars(player)

        emit("connection", player, to=room)
        print(f"{player['name']} joined room {room}")

    @socketio.on("disconnect")
    def disconnect():
        room = session.get("room")
        player = json.loads(session.get("player"))
        if not room or not player:
            return
        if room not in rooms:
            leave_room(room)
            return

        curr_game = find_game(room)  # room === pin in session
        curr_game.del_player(int(player["id"]))

        leave_room(room)

        if player['is_owner']:
            # emitting that dest enable passing reason why redirecting (it will be visible by click on browser link)
            destination = 'choose?msg=Owner of the room has left'   # it is necessary to show info alert for another players
            emit('redirect', destination, to=room)
            del_room(room)
        else: emit("disconnection", player, to=room)
        print(f"{player['name']} left room {room}")

    return app, socketio
