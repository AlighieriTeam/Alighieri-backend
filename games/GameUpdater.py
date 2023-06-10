
class GameUpdater(object):
    def __init__(self, room, socketio):
        self.__room = room
        self.__socketio = socketio

    def update_scores(self, players: list):
        ''' This method update player scores '''
        self.__socketio.emit("updateScores", players, to=self.__room)

    def show_popup(self, players: list):
        ''' This method send player scores to room and shows popup '''
        self.__socketio.emit("showPopup", players, to=self.__room)

    def start_game(self, data, destination):
        self.__socketio.emit("bot_start", data, to=destination)

    def ask_for_action(self, actions, destination, callback):
        self.__socketio.emit("bot_ask", actions, to=destination, callback=callback)

    def update_game_state(self, updates):
        self.__socketio.emit("game_update", updates, to=f"_{self.__room}")

