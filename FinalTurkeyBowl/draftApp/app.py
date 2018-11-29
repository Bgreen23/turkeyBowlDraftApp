from flask import Flask, jsonify, request, render_template, redirect
import os
import requests
import json
import pusher
from database import db_session
from models import Draft

app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id='628052',
    key='2c712e9027d8604455b8',
    secret='a7e5e6f8846b3620a7b0',
    cluster='us2',
    ssl=True)

# Lines 18-20 are how the routes should look connected to the API
# @app.route('/some-url')
# def get_data():
#     return requests.get('http://localhost:1234/api/players').content

@app.route('/')
def start():
    # players = Draft.query.all()
    # return render_template('index.html', players=players)
    return render_template('start.html')

@app.route('/index')
def index():
     players = Draft.query.all()
     return render_template('index.html', players=players)

@app.route('/backend', methods=["POST", "GET"])
def backend():
    if request.method == "POST":
        player = request.form["player"]
        team = request.form["team"]
        new_player = Draft(player, team)
        db_session.add(new_player)
        db_session.commit()

        data = {
            "id": new_player.id,
            "player": player
            }

        pusher_client.trigger('table', 'new-record', {'data': data})

        return redirect("/backend", code=302)
    else:
        players = Draft.query.all()
        return render_template('backend.html', players=players)

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        player = request.form["player"]
        team = request.form["team"]

        update_player = Draft.query.get(id)
        update_player.player = player
        update_player.team = team
        db_session.commit()

        data = {
            "id": id,
            "player": player,
            "team": team
            }

        pusher_client.trigger('table', 'update-record', {'data': data})

        return redirect("/backend", code=302)
    else:
        new_player = Draft.query.get(id)

        return render_template('update_player.html', data=new_player)

@app.route('/delete/<int:id>', methods=["DELETE"])
def delete_record(id):
    delPlayer= [ player for player in Draft if player['id'] == id]
    Draft.remove(delPlayer[0])
    db_session.commit()

    data = {
        "id": id,
        "player": player,
        "team": team
        }

    pusher_client.trigger('table', 'delete-record', {'data': data})

    return redirect("/backend", code=302)


# Code for Heroku Logging
class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

    import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


# @app.route('/jedi/<string:name>', methods=['DELETE'])
# def delete(name):
#     jed = [jedi for jedi in Jedi if jedi['name'] == name]
#     Jedi.remove(jed[0])
#     return jsonify({'Jedi' : Jedi})


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# run Flask app
if __name__ == "__main__":
    app.run()
