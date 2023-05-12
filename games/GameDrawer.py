from flask_socketio import emit, join_room, SocketIO

class GameDrawer(object):
    def __init__(self, room, socketio):
        self.__room = room
        self.__socketio = socketio

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
        self.__socketio.emit("drawRectangle", data, to=self.__room)

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
        self.__socketio.emit("drawCircle", data, to=self.__room)

    def draw_text(self, x: int, y: int, text: str):
        print("draw_text called with arguments: {} {} {} ".format(x, y, text))
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "text": text
        }
        print(data)
        self.__socketio.emit("drawText", data, to=self.__room)

    def clear_all(self):
        print("clear_all called")
        #join_room(self.__room)
        self.__socketio.emit("clearAll", to=self.__room)