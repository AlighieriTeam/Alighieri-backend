from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)
@views.route('/')
@views.route('/home')
def home_page():

    return render_template("home.html")

@views.route('/room', methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        from .room import Room
        from . import active_games as games, find_game
        from website.Player import Player
        import random

        while True:
            pin = str(random.randint(1000, 9999))
            is_game = list(filter(lambda x: x.pin == pin, games))   # check if game pin is unique
            if len(is_game) == 0:
                game_type = request.form.get('game')
                new_game = Room(pin, game_type) # create new game with given pin and type

                owner_id = len(new_game.players) + 1  # set id as num of players of new game + 1
                owner = Player(id=owner_id, name="Owner", owner=True)   # create game owner
                new_game.add_player(owner)  # add game owner to created game

                games.append(new_game)  # add this game to all games
                break

        return render_template("room.html", players=new_game.players, game_pin=pin)

    # if tried to enter /room directly - redirect to choose
    return redirect(url_for('.choose'))


@views.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        from . import find_game
        from website.Player import Player

        pin = request.form.get('pin')
        curr_game = find_game(pin)  # get current game from games by pin

        if curr_game is None:
            return redirect(url_for('.choose'))
        else:
            player_id = len(curr_game.players) + 1  # generate id
            new_player = Player(id=player_id, name=("Anon " + str(player_id - 1)))  # create player
            curr_game.add_player(new_player)    # add player to current game
            return render_template("join.html", players=curr_game.players, game_pin=pin)

    # if tried to enter /join directly - redirect to choose
    return redirect(url_for('.choose'))

@views.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method =='POST':
        from . import active_games
        pin = request.form.get('pin')
        game_list = list(filter(lambda x: x.pin == pin, active_games))
        # if game does not exist
        if len(game_list) == 0:
            # TODO: throw error with flash
            return render_template("choose.html")

        # TODO: redirect to game page
        pass
    return render_template("choose.html")

@views.route('/game')
def game():
    from .room import MOCK_PLAYERS
    return render_template("game.html", players=MOCK_PLAYERS)    # pass player list of object to subsite