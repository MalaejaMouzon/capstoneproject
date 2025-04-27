from datetime import datetime
from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    current_player = db.Column(db.String(1), default='X')
    board_state = db.Column(db.String(9), default=' ' * 9)
    game_status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, draw
    winner = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    player1 = db.relationship('User', foreign_keys=[player1_id])
    player2 = db.relationship('User', foreign_keys=[player2_id])
    winning_player = db.relationship('User', foreign_keys=[winner])

    def make_move(self, position, player):
        if self.game_status != 'in_progress':
            return False
        
        if self.current_player != player:
            return False

        if position < 0 or position >= 9:
            return False

        board = list(self.board_state)
        if board[position] != ' ':
            return False

        board[position] = player
        self.board_state = ''.join(board)
        
        if self.check_winner():
            self.game_status = 'completed'
            self.winner = self.player1_id if player == 'X' else self.player2_id
            self.completed_at = datetime.utcnow()
        elif self.check_draw():
            self.game_status = 'completed'
            self.completed_at = datetime.utcnow()
        else:
            self.current_player = 'O' if player == 'X' else 'X'

        db.session.commit()
        return True

    def check_winner(self):
        board = self.board_state
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            if (board[combo[0]] != ' ' and 
                board[combo[0]] == board[combo[1]] == board[combo[2]]):
                return True
        return False

    def check_draw(self):
        return ' ' not in self.board_state 