from flask import render_template, request, redirect, url_for, session, request
from .models import Player, db, Session, Game
from sqlalchemy.exc import IntegrityError
from ttt_app import app


@app.route('/')
def index():
    if 'player_id' in session and Session.query.filter_by(player_id=session['player_id']).all() == []:
        session['stats_button'] = 'disabled'
    else:
        session['stats_button'] = 'enabled'
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        player = Player(name=name)
        player.set_password(password)
        try:
            db.session.add(player)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            error_message = 'Name already exists'
            return render_template('register.html', error_message=error_message)

    return render_template('register.html', error_message=error_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        player = Player.query.filter_by(name=name).first()
        if player and player.check_password(password):
            session['player_id'] = player.id
            return redirect(url_for('index'))
        else:
            error_message = 'Invalid username or password'

    return render_template('login.html', error_message=error_message)
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/play', methods=['GET', 'POST'])
def play():
    if 'player_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        pass
    return render_template('play.html', session=session)


@app.route('/stats')
def get_stats_data():
    player = Player.query.filter_by(id=session['player_id']).first()
    

    # Player's overall stats
    sessions_played = len(player.sessions)
    games_played = Game.query.join(Session).filter(Session.player_id == player.id).count()

    # If the last session or game is still in progress, don't count it
    if player.sessions[-1].outcome is None:
        sessions_played -= 1
    if player.sessions[-1].games_played[-1].outcome is None:
        games_played -= 1
    
    session_win_ratio = len(Session.query.filter_by(player_id=player.id, outcome='win').all()) / sessions_played
    game_win_ratio = len(Game.query.join(Session).filter(Session.player_id == player.id, Game.outcome == 'win').all()) / games_played


    stats_data = Session.query.filter_by(player_id=player.id).all()

    # Prepare the response data
    response = {
        'player_stats': {
            'sessions_played': sessions_played,
            'games_played': games_played,
            'session_win_ratio': f'{session_win_ratio * 100:.1f}%',
            'game_win_ratio': f'{game_win_ratio * 100:.1f}%'
        },
        'stats_data': []
    }

    # Iterate over session stats data and fetch corresponding game stats
    for session_data in stats_data:
        if session_data.outcome is not None:
            session_stats = {
                'session_start_date': session_data.start_date.strftime('%d/%m/%Y'),
                'session_outcome': session_data.outcome,
                'number_of_games_in_session': len(session_data.games_played),
                'games': []
            }

            for game_data in session_data.games_played:
                if game_data.game_end is not None:
                    game_stats = {
                        'game_start': game_data.game_start.strftime('%H:%M:%S'),
                        'game_outcome': game_data.outcome,
                        'game_time': (game_data.game_end - game_data.game_start).seconds

                    }
                session_stats['games'].append(game_stats)

            response['stats_data'].append(session_stats)
    
    # Get the days on which the player played
    days = []
    for session_data in stats_data:
        if session_data.start_date.strftime('%d/%m/%Y') not in days:
            days.append(session_data.start_date.strftime('%d/%m/%Y'))
        
    session['stats_data'] = response['stats_data']

    return (render_template('stats.html', player=player, player_stats=response['player_stats'], session_stats=response['stats_data'], days=days))