

games = ['pac-man', 'pong']
class Game:
    def __init__(self, pin : str, game_type : str):
        assert 3 < len(pin) < 10
        assert game_type in games

        self.pin = pin
        self.game_type = game_type
