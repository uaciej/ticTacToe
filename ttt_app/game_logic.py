import random

class TTTGame:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        
    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.check_for_winner()
            if self.current_player == 'X':
                self.current_player = 'O'
            else:
                self.current_player = 'X'
        
        else:
            raise ValueError('Invalid move')
        
    def check_for_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                self.winner = self.board[i][0]
                self.game_over = True
                return
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                self.winner = self.board[0][i]
                self.game_over = True
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[0][0]
            self.game_over = True
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winner = self.board[0][2]
            self.game_over = True
            return
        if ' ' not in self.board[0] and ' ' not in self.board[1] and ' ' not in self.board[2]:
            self.game_over = True
            return
        
    def make_ai_move(self):
        if self.current_player == 'O' and not self.game_over:
            # Generate a random move for the AI player
            available_moves = []
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        available_moves.append((row, col))

            if available_moves:
                row, col = random.choice(available_moves)
                self.make_move(row, col)

    def __str__(self):
        return f'{self.board[0][0]}|{self.board[0][1]}|{self.board[0][2]}\n-----\n{self.board[1][0]}|{self.board[1][1]}|{self.board[1][2]}\n-----\n{self.board[2][0]}|{self.board[2][1]}|{self.board[2][2]}'
    
    def __repr__(self):
        return f'TTTGame(board={self.board}, current_player={self.current_player}, winner={self.winner}, game_over={self.game_over})'
    
    