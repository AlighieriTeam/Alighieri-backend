import json
from threading import Thread

from flask import session, url_for
from flask_socketio import join_room, leave_room, emit

from games.GameDrawer import GameDrawer
from games.pacman import PacmanController
from website import find_game, rooms, del_room


def register_room_events(app, socketio):

    def start_game(room, io):
        with app.test_request_context():
            game_drawer = GameDrawer(room, io)
            game_controller = PacmanController('pacman', game_drawer)
            game_controller.tick()

    @socketio.on("rejoin")
    def rejoin():
        ''' We need to join again to room, because redirection from room/join to game automatically leaves the room '''
        room = session.get("room")
        join_room(room)
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

        # temporary 2nd condition for presentation
        if not curr_game.started:
            if player['is_owner']:
                # emitting that dest enable passing reason why redirecting (it will be visible by click on browser link)
                destination = 'choose?msg=Owner of the room has left'  # it is necessary to show info alert for another players
                emit('redirect', destination, to=room)
                del_room(room)
            else:
                curr_game.del_player(int(player["id"]))
                leave_room(room)
                emit("disconnection", player, to=room)
                return

        print(f"{player['name']} left room {room}")

    @socketio.on('start_game')
    def get_start_signal():
        room = session.get("room")
        player = json.loads(session.get("player"))
        if not room or not player or not player['is_owner']:
            return
        if room not in rooms:
            leave_room(room)
            return
        curr_game = find_game(room)
        curr_game.started = True
        game_thread = Thread(target=start_game, args=(room, socketio))
        game_thread.start()
        socketio.emit('redirect', url_for('views.game'), to=room)

    @socketio.on("add_bot")
    def add_bot(bot_data):
        room = session.get("room")
        if room not in rooms:
            leave_room(room)
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
            return

        curr_game = find_game(room)  # room === pin in session
        curr_game.del_player(int(player["id"]))

        destination = 'choose?msg=You ware kicked by owner of the room'  # it is necessary to show info alert for another players
        emit('kick', {"dest": destination, "id": player["id"]}, to=room)
        print(f"{player['name']} was kicked from {room}")
