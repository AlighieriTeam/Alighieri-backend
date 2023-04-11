# Each game type has assigned max number of players
import random
import json

GAME_TYPES = {
    'pac-man': 4,
    'pong': 2
}


class Player:  # simple player class to show players in game page automatically
    def __init__(self, id, name, is_owner=False):
        self.id = id
        self.name = name
        self.is_owner = is_owner

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

PLAYER_NICKNAMES = ['lion', 'tiger', 'leopard', 'cheetah', 'jaguar', 'panther', 'lynx', 'bobcat', 'ocelot',
                    'serval', 'elephant', 'rhinoceros', 'hippopotamus', 'giraffe', 'zebra', 'hyena', 'wolf', 'coyote',
                    'fox', 'bear', 'polar bear', 'grizzly bear', 'black bear', 'koala', 'kangaroo', 'wallaby', 'wombat',
                    'platypus', 'crocodile', 'alligator', 'turtle', 'snake', 'python', 'cobra', 'anaconda', 'tortoise',
                    'chameleon', 'iguana', 'lizard', 'gecko', 'frog', 'toad', 'newt', 'salamander', 'shark', 'whale',
                    'dolphin', 'seal', 'otter', 'penguin', 'seagull']

MOCK_PLAYERS = [Player(1, "Jacek"), Player(2, "Placek"), Player(3, "Yan"), Player(4, "Covalaki")]


def generate_nicks(number_of_players):
    return random.sample(PLAYER_NICKNAMES, number_of_players)


class Room:
    def __init__(self, game_type: str):
        assert game_type in GAME_TYPES

        self.game_type = game_type
        self.players: list[Player] = []
        self.names = generate_nicks(GAME_TYPES[game_type])

    def add_player(self, is_owner=False) -> Player | None:
        if len(self.players) >= GAME_TYPES.get(self.game_type):  # check at first, don't make unnecessary operation
            return None
        occupied_ids = set(player.id for player in self.players)  # get all occupied ids in Room
        avail_ids = set(i for i in range(GAME_TYPES.get(self.game_type)))  # get all available ids based on game type
        player_id = list(avail_ids - occupied_ids)[0]  # get first free id
        player = Player(player_id, self.names[player_id], is_owner=is_owner)
        self.players.append(player)
        return player

    def del_player(self, id: int):
        for player in self.players:
            if player.id == id:
                self.players.remove(player)
                break
