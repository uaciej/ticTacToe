from .extensions import socketio
from .game_logic import TTTGame
from flask_socketio import emit

@socketio.on('game_start')
def handle_game_start():
    global GAME
    GAME = TTTGame()
    emit('move', {'board': GAME.board}, broadcast=True)

@socketio.on('make_move')
def handle_make_move(data):
    row = data['row']
    col = data['col']

    GAME.make_move(row, col)

    emit('move', {'board': GAME.board, 'game_over': GAME.game_over, 'winner': GAME.winner}, broadcast=True)

@socketio.on('game_over')
def handle_game_over(data):
    emit('result', {'winner': data['winner']}, broadcast=True)

