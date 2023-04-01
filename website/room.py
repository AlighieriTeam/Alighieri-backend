from website.Player import Player

# Each game type has assigned max number of players
GAME_TYPES = {
    'pac-man': 4,
    'pong': 2
}

MOCK_PLAYERS = [Player(1, "Jacek"), Player(2, "Placek"), Player(3, "Yan"), Player(4, "Covalaki")]

class Room:
    def __init__(self, pin: str, game_type: str):
        assert 3 < len(str(pin)) < 10
        assert game_type in GAME_TYPES

        self.pin = pin
        self.game_type = game_type
        self.players: list[Player] = []

    def add_player(self, player: Player):
        if len(self.players) <= GAME_TYPES.get(self.game_type):
            self.players.append(player)
