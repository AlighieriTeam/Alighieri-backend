from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)
@views.route('/')
@views.route('/home')
def home_page():

    return render_template("home.html")

@views.route('/room', methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        from .room import generate_nicks, Room, GAME_TYPES
        from . import active_games as games
        import random
        while True:
            pin = str(random.randint(1000, 9999))
            is_game = list(filter(lambda x: x.pin == pin, games))
            if len(is_game) == 0:
                game_type = request.form.get('game')
                games.append(Room(pin, game_type))
                break
        return render_template("room.html", players=generate_nicks(GAME_TYPES[game_type]), game_pin=pin)

    # if tried to enter /room directly - redirect to choose
    return redirect(url_for('.choose'))


@views.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        from .room import MOCK_PLAYERS

        pin = request.form.get('pin')
        from . import active_games as games
        is_game = list(filter(lambda x: x.pin == pin, games))
        if len(is_game) == 0:
            return redirect(url_for('.choose'))
        return render_template("join.html", players=MOCK_PLAYERS, game_pin=pin)

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