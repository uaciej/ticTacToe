from flask import render_template, request, redirect, url_for, session
from .models import Player, db
from sqlalchemy.exc import IntegrityError
from ttt_app import app


@app.route('/')
def index():
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

