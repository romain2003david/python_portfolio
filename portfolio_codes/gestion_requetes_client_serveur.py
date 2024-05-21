from flask import Flask, request, url_for, redirect
from pymongo import MongoClient
import os


app = Flask(__name__)

client = MongoClient('localhost', 27017)

data_base = client.flask_db

todos = data_base.players


class Player:

    def __init__(self, name, last_name, age):

        self.name = name

        self.last_name = last_name

        self.age = age

    def __str__(self):

        return "Player info : {} {}, {} ans\n".format(self.name, self.last_name, self.age)


@app.route('/')
def all_players():
    return 'Hello, World!'


@app.route('/import', methods=['GET', 'POST'])
def import_def():
    if request.method == 'POST':
        return "objet post"
    else:
        cmd = 'python3 /home/ubuntu/flask/test.py >> /home/ubuntu/flask/data.dat'
        os.system(cmd)
        return "objet get"


@app.route('/import/<object>', methods=['GET', 'POST'])
def import_def(object):
