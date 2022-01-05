from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import pyaes
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    passw = db.Column(db.String(100))


    def __init__(self, user, passw):
        self.user = user
        self.passw = passw

db.create_all()
@app.route('/Login')
def Login():

    return render_template("login.html")

@app.route('/Register')
def Register():
    return render_template("registration.html")

@app.route('/Index')
def Index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)