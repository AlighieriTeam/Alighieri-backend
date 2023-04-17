from flask import Blueprint, render_template, request, redirect, url_for, session, json, flash

from . import find_game, cfg

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
        player = curr_game.add_player(is_owner=True)

        rooms[pin] = curr_game

        session['room'] = pin
        session['player'] = player.to_json()

        players = [p.to_json() for p in curr_game.players]

        return render_template("room.html", players=players, bots=cfg.avail_bots, game_pin=pin)

    # if tried to enter /room directly - redirect to choose
    return redirect(url_for('.choose'))

@views.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        from . import rooms

        pin = request.form.get('pin')
        curr_game = find_game(pin)

        if curr_game is None:
            flash('Room with given id does not exist', 'alert-danger')  # second parameter must be existing class in BootStrap !
            return redirect(url_for('.choose'))

        r = session.get('room')
        if r == pin:
            return render_template("join.html", players=[p.to_json() for p in curr_game.players], game_pin=pin)

        if curr_game.started:
            flash('Game already started', 'alert-danger')  # second parameter must be existing class in BootStrap !
            return redirect(url_for('.choose'))

        player = curr_game.add_player()
        if not player:
            flash('Room is full', 'alert-info')
            return redirect(url_for('.choose'))

        rooms[pin] = curr_game

        session['room'] = pin
        session['player'] = player.to_json()

        players = [p.to_json() for p in curr_game.players]

        return render_template("join.html", players=players, actual_player_id=player.id, game_pin=pin)

    # if tried to enter /join directly - redirect to choose
    return redirect(url_for('.choose'))

@views.route('/choose')
def choose():
    msg = request.args.get('msg')
    if msg: flash(msg, 'alert-info')
    # cannot clear session (flashing not work), but can clear room associated wth session to keep no duplicating player during refresh
    # Solutions
    # 1. left it like it is, clearing only room associated with session and keep flasking working
    # 2. clear whole session and flashing not work, so we will need to write our own popups with info for players
    session['room'] = None
    return render_template("choose.html")

@views.route('/game')
def game():
    from .room import MOCK_PLAYERS
    return render_template("game.html", players=MOCK_PLAYERS)    # pass player list of object to subsite