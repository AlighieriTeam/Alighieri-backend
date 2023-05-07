from flask_socketio import emit, join_room, SocketIO

import main

class GameDrawer(object):
    socketio = main.SOCKETIO
    def __init__(self, session):
        self.__session = session
        self.__room = self.__session.get("room")

    def draw_rectangle(self, x: int, y: int, color: str, width: int, height: int):
        print("draw_rectangle called with arguments: {} {} {} {} {}".format(x, y, color, width, height))
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "color": color,
            "width": width,
            "height": height
        }
        print(data)
        main.SOCKETIO.emit("drawRectangle", data, to=self.__room)

    def draw_circle(self, x: int, y: int, color: str, radius: int):
        print("draw_circle called with arguments: {} {} {} {}".format(x, y, color, radius))
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "color": color,
            "radius": radius
        }
        print(data)
        main.SOCKETIO.emit("drawCircle", data, to=self.__room)

    def draw_text(self, x: int, y: int, text: str):
        print("draw_text called with arguments: {} {} {} ".format(x, y, text))
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "text": text
        }
        print(data)
        main.SOCKETIO.emit("drawText", data, to=self.__room)

    def clear_all(self):
        print("clear_all called")
        #join_room(self.__room)
        main.SOCKETIO.emit("clearAll", to=self.__room)