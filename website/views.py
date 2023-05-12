import threading

from flask import Blueprint, render_template, request, redirect, url_for, session, json, flash

from games.GameDrawer import GameDrawer
from games.pacman import PacmanController
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
    room = session.get('room')
    player = json.loads(session.get("player"))
    curr_game = find_game(room)
    if not room or not player:
        flash('You aren\'t assigned to this room', 'alert-danger')
        return redirect(url_for('.choose'))
    if not curr_game:
        flash('Room with given id does not exist', 'alert-danger')
        return redirect(url_for('.choose'))
    if not curr_game.started:
        flash('Game has not started yet', 'alert-danger')
        return redirect(url_for('.choose'))

    print(player)

    if player['is_owner']:
        print("can start pacman")
        # def start_game():
        #     with main.APP.test_request_context():
        #         game_drawer = GameDrawer(session=session)
        #         game_controller = PacmanController('pacman', game_drawer)
        #         game_controller.tick()
        # game_thread = threading.Thread(target=start_game)
        # game_thread.start()

    return render_template('game.html', players=curr_game.players)
