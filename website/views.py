from flask import Blueprint, render_template, request, redirect, url_for, session

from . import find_game

views = Blueprint('views', __name__)
@views.route('/')
@views.route('/home')
def home_page():

    return render_template("home.html")

@views.route('/room', methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        from .room import Room
        from . import rooms
        import random
        while True:
            pin = str(random.randint(1000, 9999))
            curr_game = find_game(pin)
            if curr_game is None:
                break

        game_type = request.form.get('game')
        curr_game = Room(game_type)
        player = curr_game.add_player()

        rooms[pin] = curr_game

        session['room'] = pin
        session['player'] = player.to_json()

        return render_template("room.html", players=curr_game.players, game_pin=pin)

    # if tried to enter /room directly - redirect to choose
    return redirect(url_for('.choose'))


@views.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        from . import rooms

        pin = request.form.get('pin')
        curr_game = find_game(pin)
        if curr_game is None:
            return redirect(url_for('.choose'))

        player = curr_game.add_player()

        rooms[pin] = curr_game

        session['room'] = pin
        session['player'] = player.to_json()

        return render_template("join.html", players=curr_game.players, game_pin=pin)

    # if tried to enter /join directly - redirect to choose
    return redirect(url_for('.choose'))

@views.route('/choose')
def choose():
    session.clear()
    return render_template("choose.html")

@views.route('/game')
def game():
    from .room import MOCK_PLAYERS
    return render_template("game.html", players=MOCK_PLAYERS)    # pass player list of object to subsite