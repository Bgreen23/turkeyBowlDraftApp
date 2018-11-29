from flask import Flask, request, jsonify, render_template, redirect
import os
import json
import pusher
from database import db_session
from models import Draft
api = Flask(__name__)

Team = [{'name' : 'Team Green'}, {'name' : 'Team Dostal'}, {'name' : 'Undrafted'}]

#GET Players
@api.route('/api/players')
def index():
     players = Draft.query.all()
     return render_template('index.html', players=players)

#GET Teams
@api.route('/api/team')
def team():
    team = Draft.query.all()
    return jsonify({'Team' : Team})

#GET Players in Team Green
@api.route('/api/team/<string:name>', methods=['GET'])
def teamgreen(team):
    tea = [team for team in Team if team['name'] == name]
    return jsonify({'name' : tea[0]})



# #GET request
# @app.route('/jedi' , methods=['GET'])
# def showall():
#     return jsonify({'Jedi' : Jedi})
# @app.route('/jedi/<string:name>', methods=['GET'])
# def show(name):
#     jed = [jedi for jedi in Jedi if jedi['name'] == name]
#     return jsonify({'jedi' : jed[0]})
#
# @app.route('/jedi' , methods=['POST'])
# def add():
#     jedi = {'name' : request.json['name']}
#     Jedi.append(jedi)
#     return jsonify({'jedi' : jedi})
#
# #PUT request
# @app.route('/jedi/<string:name>', methods=['PUT'])
# def edit(name):
#     jed = [jedi for jedi in Jedi if jedi['name'] == name]
#     jedi[0]['names'] = request.json['name']
#     return jsonify({'jedi' : jed[0]})
#
# #DELETE request
# @app.route('/jedi/<string:name>', methods=['DELETE'])
# def delete(name):
#     jed = [jedi for jedi in Jedi if jedi['name'] == name]
#     Jedi.remove(jed[0])
#     return jsonify({'Jedi' : Jedi})
