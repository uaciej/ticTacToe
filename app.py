from ttt_app import app, db, socketio
from ttt_app.migrations import migrate

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        migrate.init_app(app, db)
        socketio.run(app, host="0.0.0.0")