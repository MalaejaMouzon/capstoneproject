from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.game import Game
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('game.lobby'))
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    games = Game.query.filter(
        (Game.player1_id == current_user.id) | 
        (Game.player2_id == current_user.id)
    ).order_by(Game.created_at.desc()).limit(10).all()
    
    stats = {
        'games_played': current_user.games_played,
        'games_won': current_user.games_won,
        'games_lost': current_user.games_lost,
        'games_drawn': current_user.games_drawn,
        'win_rate': (current_user.games_won / current_user.games_played * 100 
                    if current_user.games_played > 0 else 0)
    }
    
    return render_template('profile.html', games=games, stats=stats) 