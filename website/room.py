# Each game type has assigned max number of players
import random
import json
from threading import Thread
from typing import Optional
import time
import threading

from games.pacman import PacmanController

GAME_TYPES = {
    'pac-man': 4,
    'pong': 2
}


def generate_token_for_player():
    chars = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    token_l = random.choices(chars, k=10)
    token = ''.join(s for s in token_l)
    return token


class Player:  # simple player class to show players in game page automatically
    def __init__(self, id, name, is_owner=False, is_bot=False):
        self.id = id
        self.name = name
        self.is_owner = is_owner
        self.is_bot = is_bot
        self.points = 0
        self.token = generate_token_for_player()

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
        self.started = False
        self._game_thread: Optional[Thread] = None
        self._game_controller: Optional[PacmanController] = None
        self._timer = None

    def add_player(self, name=None, is_owner=False, is_bot=False) -> Player | None:
        if len(self.players) >= GAME_TYPES.get(self.game_type):  # check at first, don't make unnecessary operation
            return None
        occupied_ids = set(player.id for player in self.players)  # get all occupied ids in Room
        avail_ids = set(i for i in range(GAME_TYPES.get(self.game_type)))  # get all available ids based on game type
        player_id = list(avail_ids - occupied_ids)[0]  # get first free id
        if name is None:
            player = Player(id=player_id, name=self.names[player_id], is_owner=is_owner, is_bot=is_bot)
        else:
            player = Player(id=player_id, name=name, is_owner=is_owner, is_bot=is_bot)
        self.players.append(player)
        return player

    def del_player(self, id: int):
        for player in self.players:
            if player.id == id:
                self.players.remove(player)
                break

    def get_player_dict_list(self):
        return [vars(p) for p in self.players]

    def move_game_to_room_thread(self, th):
        self._game_thread = th

    def set_controller(self, controller):
        if not self._game_controller:
            self._game_controller = controller

    def start_game(self):
        if self._game_thread:
            self._game_thread.start()
            self._timer = Timer(1)

    def is_rejoinable(self):
        return not self._timer.check_time()

    def stop_game(self):
        if self._game_thread:
            self._game_controller.stop_game()

class Timer:
    def __init__(self, interval):
        self.interval = interval
        self.start_time = None
        self.thread = threading.Thread(target=self._countdown)
        self.thread.start()

    def _countdown(self):
        self.start_time = time.time()
        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.interval:
                break
            time.sleep(0.01)

    def check_time(self):
        if self.start_time is None:
            return False
        return (time.time() - self.start_time) > self.interval

