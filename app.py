from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Player

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/ttt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ttt'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Welcome to Tic Tac Toe!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        player = Player(name=username)
        player.set_password(password)
        db.session.add(player)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        player = Player.query.filter_by(name=username).first()
        if player and player.check_password(password):
            session['player_id'] = player.id
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/play', methods=['GET', 'POST'])
def play():
    pass
    

if __name__ == '__main__':
    app.run()