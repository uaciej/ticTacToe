from flask import session
from .extensions import socketio
from .game_logic import TTTGame
from .models import Player, db, Session, Game
from flask_socketio import emit
from datetime import datetime
import time

game_state = {}

def get_player():
    return Player.query.filter_by(id=session['player_id']).first()

def get_game_session():
    return Session.query.filter_by(player_id=session['player_id']).order_by(Session.id.desc()).first()

def get_game():
    game_session = get_game_session()
    return Game.query.filter_by(session_id=game_session.id).order_by(Game.id.desc()).first()

def check_for_interrupted_game():
    game = get_game()
    if game.outcome is None:
        player = get_player()
        game.game_end = datetime.utcnow()
        game.outcome = 'tie'
        player.credits += 3
        db.session.commit()


@socketio.on('check_session')
def handle_check_session():
    player = get_player()
    session['player'] = player
    if player.sessions and player.sessions[-1].outcome is None:
        game = get_game()
        session['game_id'] = game.id
        if game_state.get(player.id) is not None:
            tttgame = TTTGame()
            tttgame.board = game_state[player.id]
            session['tttgame'] = tttgame
            emit('move', {'board': tttgame.board, 'player':player.id, 'credits': player.credits }, broadcast=True)
        else:
            check_for_interrupted_game()
            handle_game_start()
    else:
        start_new_session()


@socketio.on('game_start')
def handle_game_start():
    player = get_player()
    game_session = get_game_session()
    game = session['game'] = Game(session_id=game_session.id)
    db.session.add(game)
    session['tttgame'] = tttgame = TTTGame()
    game_state[player.id] = tttgame.board
    session['player'] = player
    if player.credits in (1, 2):
        game_session.outcome = 'lose'
        db.session.commit()
        emit('not_enough_credits', {'message': 'Not enough credits'}, broadcast=True)
        return
    player.credits -= 3
    db.session.commit()
    session['game_id'] = game.id
    emit('move', {'board': tttgame.board, 'player':player.id, 'credits': player.credits }, broadcast=True)

@socketio.on('make_move')
def handle_make_move(data):
    player = get_player()
    row = data['row']
    col = data['col']
    tttgame = session['tttgame']
    tttgame.make_move(row, col)
    emit('move', {'board': tttgame.board, 'game_over': tttgame.game_over, 'winner': tttgame.winner, 'credits': player.credits, 'current_player': tttgame.current_player}, broadcast=True)

@socketio.on('ai_move')
def handle_ai_move():
    tttgame = session['tttgame']
    player = session['player']
    time.sleep(0.5)
    tttgame.make_ai_move()
    emit('move', {'board': tttgame.board, 'game_over': tttgame.game_over, 'winner': tttgame.winner, 'credits': player.credits, 'current_player': tttgame.current_player}, broadcast=True)

@socketio.on('game_over')
def handle_game_over(data):
    game = get_game()
    player = get_player()
    game.game_end = datetime.utcnow()
    if data['winner'] == 'X':
        player.credits += 4
        game.outcome = 'win'
    if data['winner'] is None:
        player.credits += 3
        game.outcome = 'tie'
    if data['winner'] == 'O':
        game.outcome = 'loss'
    game_state[player.id] = None
    db.session.commit()
    emit('result', {'winner': data['winner'], 'credits': player.credits}, broadcast=True)

@socketio.on('add_credits')
def add_credits():
    player = get_player()
    player.credits = 10
    db.session.commit()
    emit('credits_added', {'message': 'Credits added', 'success': True, 'credits': player.credits}, broadcast=True)

@socketio.on('session_won')
def handle_session_won():
    game_session = get_game_session()
    game_session.outcome = 'win'
    db.session.commit()
    emit('session_result', {'message': 'Session won', 'success': True}, broadcast=True)

@socketio.on('start_new_session')
def start_new_session():
    player = get_player()
    game_session = session['gameSession'] = Session(player_id=player.id)
    db.session.add(game_session)
    player.credits = 10
    db.session.commit()
    handle_game_start()


@socketio.on('fetch_stats_data_by_date')
def fetch_stats_data_by_date(data):
    stats_data = [dic for dic in session['stats_data'] if dic['session_start_date'] == data['date']]
    emit('stats_data_by_date', {'stats_data': stats_data}, broadcast=True)