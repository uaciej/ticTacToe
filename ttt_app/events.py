from flask import session
from .extensions import socketio
from .game_logic import TTTGame
from .models import Player, db
from flask_socketio import emit
import time


@socketio.on('game_start')
def handle_game_start():
    game = session['game'] = TTTGame() 
    player = Player.query.filter_by(id=session['player_id']).first()
    session['player'] = player
    if player.credits < 3 and player.credits > 0:
        print('not enough credits')
        emit('not_enough_credits', {'message': 'Not enough credits'}, broadcast=True)
        return
    player.credits -= 3
    db.session.commit()
    emit('move', {'board': game.board, 'player':player.id, 'credits': player.credits }, broadcast=True)

@socketio.on('make_move')
def handle_make_move(data):
    row = data['row']
    col = data['col']
    game = session['game']
    player = session['player']

    game.make_move(row, col)
    emit('move', {'board': game.board, 'game_over': game.game_over, 'winner': game.winner, 'credits': player.credits, 'current_player': game.current_player}, broadcast=True)

@socketio.on('ai_move')
def handle_ai_move():
    game = session['game']
    player = session['player']
    time.sleep(0.5)
    game.make_ai_move()
    emit('move', {'board': game.board, 'game_over': game.game_over, 'winner': game.winner, 'credits': player.credits, 'current_player': game.current_player}, broadcast=True)

@socketio.on('game_over')
def handle_game_over(data):
    player = Player.query.filter_by(id=session['player_id']).first()
    if data['winner'] == 'X':
        player.credits += 4
        db.session.commit()
    if data['winner'] == None:
        player.credits += 3
        db.session.commit()
    
    emit('result', {'winner': data['winner'], 'credits': player.credits}, broadcast=True)

@socketio.on('add_credits')
def add_credits():
    player = Player.query.filter_by(id=session['player_id']).first()
    player.credits = 10
    db.session.commit()
    emit('credits_added', {'message': 'Credits added', 'success': True, 'credits': player.credits}, broadcast=True)

@socketio.on('start_new_session')
def start_new_session():
    player = Player.query.filter_by(id=session['player_id']).first()
    player.credits = 10
    db.session.commit()
    handle_game_start()

