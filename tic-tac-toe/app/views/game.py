from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.game import Game
from app.models.user import User
from app import db

bp = Blueprint('game', __name__)

@bp.route('/lobby')
@login_required
def lobby():
    active_games = Game.query.filter(
        (Game.player1_id == current_user.id) | 
        (Game.player2_id == current_user.id),
        Game.game_status == 'in_progress'
    ).all()
    
    available_games = Game.query.filter(
        Game.player2_id.is_(None),
        Game.game_status == 'in_progress',
        Game.player1_id != current_user.id
    ).all()
    
    return render_template('game/lobby.html', 
                         active_games=active_games,
                         available_games=available_games)

@bp.route('/game/new')
@login_required
def new_game():
    game = Game(player1_id=current_user.id)
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('game.play', game_id=game.id))

@bp.route('/game/<int:game_id>')
@login_required
def play(game_id):
    game = Game.query.get_or_404(game_id)
    
    if game.player1_id != current_user.id and game.player2_id != current_user.id:
        return redirect(url_for('game.lobby'))
    
    return render_template('game/play.html', game=game)

@bp.route('/game/<int:game_id>/join')
@login_required
def join_game(game_id):
    game = Game.query.get_or_404(game_id)
    
    if game.player2_id is not None:
        return redirect(url_for('game.lobby'))
    
    if game.player1_id == current_user.id:
        return redirect(url_for('game.play', game_id=game.id))
    
    game.player2_id = current_user.id
    db.session.commit()
    return redirect(url_for('game.play', game_id=game.id))

@bp.route('/game/<int:game_id>/move', methods=['POST'])
@login_required
def make_move(game_id):
    game = Game.query.get_or_404(game_id)
    
    if game.game_status != 'in_progress':
        return jsonify({'error': 'Game is not in progress'}), 400
    
    if (game.player1_id != current_user.id and 
        game.player2_id != current_user.id):
        return jsonify({'error': 'Not a player in this game'}), 403
    
    position = request.json.get('position')
    player = 'X' if game.player1_id == current_user.id else 'O'
    
    if not game.make_move(position, player):
        return jsonify({'error': 'Invalid move'}), 400
    
    if game.game_status == 'completed':
        if game.winner:
            winner = User.query.get(game.winner)
            winner.update_stats('win')
            loser = User.query.get(game.player2_id if game.winner == game.player1_id else game.player1_id)
            loser.update_stats('lose')
        else:
            game.player1.update_stats('draw')
            game.player2.update_stats('draw')
    
    return jsonify({
        'board': game.board_state,
        'current_player': game.current_player,
        'game_status': game.game_status,
        'winner': game.winner
    }) 