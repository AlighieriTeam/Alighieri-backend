
class GameUpdater(object):
    def __init__(self, room, socketio):
        self.__room = room
        self.__socketio = socketio

    def update_scores(self, player_scores: dict):
        # TODO: to implement, method to update player scores during the game
        pass

    def show_popup(self, player_scores: dict):
        ''' This method send player scores to room and shows popup '''
        self.__socketio.emit("showPopup", player_scores, to=self.__room)