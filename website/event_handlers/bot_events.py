from flask_socketio import emit, join_room
from flask import request, session


def register_bot_events(socketio):
    @socketio.on("bot_connect")
    def bot_connect(data):
        room_pin = None
        token = None
        try:
            room_pin = data['room']
            token = data['token']
        except KeyError as e:
            emit("bot_error", "Invalid data", to=request.sid)
            return

        if not room_pin or not token:
            emit("Invalid data", to=request.sid)
        from website import find_game
        room = find_game(room_pin)
        if room is None:
            emit("bot_error", "Invalid room pin", to=request.sid)
        for p in room.players:
            if p.token == token:
                p.sid = request.sid
                break
        join_room(f"_{room_pin}")
        session['room'] = room_pin
        emit("bot_connected", to=request.sid)

    @socketio.on("bot_answer")
    def bot_answer(data):
        room_pin = session.get('room')
        if not room_pin:
            emit("bot_error", "Invalid session", to=request.sid)
        from website import find_game
        room = find_game(room_pin)
        if not room:
            emit("bot_error", "Invalid session - not connected to any room", to=request.sid)

