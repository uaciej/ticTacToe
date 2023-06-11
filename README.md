# ticTacToe

Build and run the containers using docker-compose up -d

Access the running app container using:
docker-compose exec app bash

execute this command:
flask db stamp head --directory ttt_app/migrations && flask db migrate --directory ttt_app/migrations && flask db upgrade --directory ttt_app/migrations

Now the server can be accessed at http://127.0.0.1:5000

You start a session with 10 credits.
You play vs AI.
Each game costs 3 credits.
Win grants you 4 credits.
Tie gives you back 3 credits.
Lose gives you no credits.

Session starts you at 10 credits.
Reach 15 and you win the session.
Reach 0 and you can add 10 credits to your account.
Have 1 or 2 credits after losing a game and you lose the session.
