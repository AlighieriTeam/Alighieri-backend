

class GameDrawer(object):
    def __init__(self, room, socketio):
        self.__room = room
        self.__socketio = socketio

    def set_screen_size(self, width, height, scale):
        data = {
            "width": width,
            "height": height,
            "scale": scale
        }
        self.__socketio.emit("setScreenSize", data, to=self.__room)

    def draw_rectangle(self, x: int, y: int, color: str, width: int, height: int):
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "color": color,
            "width": width,
            "height": height
        }
        self.__socketio.emit("drawRectangle", data, to=self.__room)

    def draw_circle(self, x: int, y: int, color: str, radius: int):
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "color": color,
            "radius": radius
        }
        self.__socketio.emit("drawCircle", data, to=self.__room)

    def draw_ghost(self, x: int, y: int, color: str, width: int, height: int):
        # join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "color": color,
            "width": width,
            "height": height
        }
        self.__socketio.emit("drawGhost", data, to=self.__room)

    def draw_text(self, x: int, y: int, text: str):
        #join_room(self.__room)
        data = {
            "x": x,
            "y": y,
            "text": text
        }
        self.__socketio.emit("drawText", data, to=self.__room)

    def clear_all(self):
        #join_room(self.__room)
        self.__socketio.emit("clearAll", to=self.__room)
