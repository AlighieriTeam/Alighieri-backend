from flask import Blueprint, render_template, request, redirect, url_for, session, json, flash

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
        player = curr_game.add_player(is_owner=True)

        rooms[pin] = curr_game

        session['room'] = pin
        session['player'] = player.to_json()

        players = [p.to_json() for p in curr_game.players]

        return render_template("room.html", players=players, game_pin=pin)

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

        return render_template("join.html", players=players, game_pin=pin)

    # if tried to enter /join directly - redirect to choose
    return redirect(url_for('.choose'))

@views.route('/choose')
def choose():
    #session.clear()    # flashing does not work when session is cleared
    msg = request.args.get('msg')
    if msg: flash(msg, 'alert-info')
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

    return render_template('game.html', players=curr_game.players)
