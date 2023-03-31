

games = ['pac-man', 'pong']

class Player:   # simple player class to show players in game page automatically
    def __init__(self, id, name):
        self.id = id
        self.name = name

players = [Player(1, "Jacek"), Player(2, "Placek"), Player(3, "Yan"), Player(4, "Covalaki")]

class Room:
    def __init__(self, pin : str, game_type : str):
        assert 3 < len(str(pin)) < 10
        assert game_type in games

        self.pin = pin
        self.game_type = game_type
