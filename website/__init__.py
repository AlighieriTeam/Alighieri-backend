import json
from typing import Optional

from flask import Flask, session, url_for
from flask_socketio import join_room, leave_room, send, SocketIO, emit
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

    app.register_blueprint(views, url_prefix='/')

    @socketio.on("connected")
    def connected():
        room = session.get("room")
        player = json.loads(session.get("player"))
        if not room or not player:
            return
        if room not in rooms:
            leave_room(room)
            print("1")
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
        print("->>>>", room)
        print("->>>>", rooms)
        if room not in rooms:
            leave_room(room)
            print("2")
            return

        curr_game = find_game(room)  # room === pin in session

        # temporary 2nd condition for presentation
        if not curr_game.started:
            print("here")
            if player['is_owner']:
                # emitting that dest enable passing reason why redirecting (it will be visible by click on browser link)
                destination = 'choose?msg=Owner of the room has left'  # it is necessary to show info alert for another players
                emit('redirect', destination, to=room)
                del_room(room)
            else:
                curr_game.del_player(int(player["id"]))
                leave_room(room)
                print("3")
                emit("disconnection", player, to=room)
                return

        print(f"{player['name']} left room {room}")

    @socketio.on('start_game')
    def start_game():
        room = session.get("room")
        player = json.loads(session.get("player"))
        if not room or not player or not player['is_owner']:
            return
        if room not in rooms:
            leave_room(room)
            print("4")
            return
        curr_game = find_game(room)
        curr_game.started = True
        socketio.emit('redirect', url_for('views.game'), to=room)

    @socketio.on("add_bot")
    def add_bot(bot_data):
        room = session.get("room")
        if room not in rooms:
            leave_room(room)
            print("5")
            return

        curr_game = find_game(room)

        player = curr_game.add_player(name=bot_data['name'], is_bot=True)
        # TODO: try to inform owner that room is full, somehow by flash, disable add bot button, js alert?
        if player is None: return
        player = vars(player)

        emit("connection", player, to=room)
        print(f"{player['name']} joined room {room}")

    @socketio.on("del_player")
    def del_player(player):
        room = session.get("room")
        if room not in rooms:
            leave_room(room)
            print("6")
            return

        curr_game = find_game(room)  # room === pin in session
        curr_game.del_player(int(player["id"]))

        destination = 'choose?msg=You ware kicked by owner of the room'  # it is necessary to show info alert for another players
        emit('kick', {"dest": destination, "id": player["id"]}, to=room)
        print(f"{player['name']} was kicked from {room}")


    @socketio.on("test")
    def test():
        print("called")
        room = session.get("room")
        curr_game = find_game(room)
        print(room)
        emit("test_js", curr_game.players, to=room)


    return app, socketio
