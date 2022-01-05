from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import pyaes
import sqlite3


key_Private = RSA.generate(3072)  # 4096
key_Public = key_Private.publickey()

#with open("user_file", "wb") as c_file:
#    c_file.write(key_Private)

def encrypt_user(string):
        encoded = string.encode()
        result1 = hashlib.sha256(encoded)
        a= result1.hexdigest()
        b = bytes(a, 'utf-8')
        encryptor = PKCS1_OAEP.new(key_Public)
        encrypted = encryptor.encrypt(b)
        return encrypted
def decrypt_user(encrypted):
    decryptor = PKCS1_OAEP.new(key_Private)
    decrypted = decryptor.decrypt(encrypted)
    return decrypted
def SHA(userx):
    encoded = userx.encode()
    result2 = hashlib.sha256(encoded)
    a = result2.hexdigest()
    return a

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    passw = db.Column(db.String(100))


    def __init__(self, user, passw):
        self.user = user
        self.passw = passw

db.create_all()

@app.route('/Register', methods=['GET','POST'])
def Register():
    return render_template("registration.html")
@app.route('/')
def insert():
    if request.method == 'POST':

            account = Account(encrypt_user(request.form['user']), encrypt_user(request.form['password']))
            db.session.add(account)
            db.session.commit()
            flash("Inserted Successfully")
            return redirect(url_for('Register'))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
