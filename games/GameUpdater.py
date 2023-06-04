
class GameUpdater(object):
    def __init__(self, room, socketio):
        self.__room = room
        self.__socketio = socketio

    def update_scores(self, players: dict):
        self.__socketio.emit("updateScores", players, to=self.__room)

    def show_popup(self, players: list):
        ''' This method send player scores to room and shows popup '''
        self.__socketio.emit("showPopup", players, to=self.__room)