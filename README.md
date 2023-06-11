# ticTacToe

Build and run the containers using docker-compose up -d

Access the running app container using:
docker-compose exec app bash

execute this command:
flask db stamp head --directory ttt_app/migrations && flask db migrate --directory ttt_app/migrations && flask db upgrade --directory ttt_app/migrations

Now the server can be accessed at http://127.0.0.1:5000
