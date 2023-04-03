# Each game type has assigned max number of players
import random

GAME_TYPES = {
    'pac-man': 4,
    'pong': 2
}


class Player:  # simple player class to show players in game page automatically
    def __init__(self, id, name):
        self.id = id
        self.name = name


PLAYER_NICKNAMES = ['lion', 'tiger', 'leopard', 'cheetah', 'jaguar', 'panther', 'lynx', 'bobcat', 'ocelot',
                              'serval', 'elephant','rhinoceros','hippopotamus','giraffe','zebra','hyena','wolf','coyote',
                              'fox','bear','polar bear','grizzly bear','black bear','koala','kangaroo','wallaby','wombat',
                              'platypus','crocodile','alligator','turtle','snake','python','cobra','anaconda','tortoise',
                              'chameleon','iguana','lizard','gecko','frog','toad','newt','salamander','shark','whale',
                              'dolphin','seal','otter','penguin','seagull']

MOCK_PLAYERS = [Player(1, "Jacek"), Player(2, "Placek"), Player(3, "Yan"), Player(4, "Covalaki")]

def generate_nicks(number_of_players):
    nicknameset = random.sample(range(0,len(PLAYER_NICKNAMES)),number_of_players)
    playernicks = []
    for i in range(0,number_of_players):
        playernicks.append(Player(i+1,PLAYER_NICKNAMES[nicknameset.pop()]))
    return playernicks

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
