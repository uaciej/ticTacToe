from ..game_logic import TTTGame

# create tests for the TTTGame class
def test_game_init():
    game = TTTGame()
    assert game.board == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game.current_player == 'X'
    assert game.game_over == False
    assert game.winner == None

def test_make_move():
    game = TTTGame()
    game.make_move(0, 0)
    assert game.board == [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game.current_player == 'O'
    assert game.game_over == False
    assert game.winner == None

def test_make_move_2():
    game = TTTGame()
    game.make_move(0, 0)
    game.make_move(0, 1)
    assert game.board == [['X', 'O', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game.current_player == 'X'
    assert game.game_over == False
    assert game.winner == None


def test_make_move_win():
    game = TTTGame()
    game.make_move(0, 0)
    game.make_move(0, 1)
    game.make_move(1, 0)
    game.make_move(0, 2)
    game.make_move(2, 0)
    assert game.board == [['X', 'O', 'O'], ['X', ' ', ' '], ['X', ' ', ' ']]
    assert game.current_player == 'O'
    assert game.game_over == True
    assert game.winner == 'X'
