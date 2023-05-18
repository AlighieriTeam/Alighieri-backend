from flask import session
from flask_socketio import join_room, leave_room, emit

def register_game_events(socketio):

    @socketio.on("draw_rectangle")
    def draw_rectangle(x: int, y: int, color: str, width: int, height: int):
        print("draw_rectangle called with arguments: {} {} {} {} {}".format(x, y, color, width, height))
        room = session.get("room")
        data = {
            "x": x,
            "y": y,
            "color": color,
            "width": width,
            "height": height
        }
        print(data)
        emit("drawRectangle", data, to=room)

    @socketio.on("draw_circle")
    def draw_circle(x: int, y: int, color: str, radius: int):
        print("draw_circle called with arguments: {} {} {} {}".format(x, y, color, radius))
        room = session.get("room")
        data = {
            "x": x,
            "y": y,
            "color": color,
            "radius": radius
        }
        print(data)
        emit("drawCircle", data, to=room)

    @socketio.on("draw_text")
    def draw_text(x: int, y: int, text: str):
        print("draw_text called with arguments: {} {} {} ".format(x, y, text))
        room = session.get("room")
        data = {
            "x": x,
            "y": y,
            "text": text
        }
        print(data)
        emit("drawText", data, to=room)

    @socketio.on("clear_all")
    def clear_all():
        print("clear_all called")
        room = session.get("room")
        emit("clearAll", to=room)
