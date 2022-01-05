from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from Crypto.Random import get_random_bytes
from base64 import b64encode
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import pyaes
import sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Danhba.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

key_r = get_random_bytes(22)
key = b64encode(key_r)
key_Private = RSA.generate(3072)  # 4096
key_Public = key_Private.publickey()


def encrypt(plaintext):
    cipher = AES.new(key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext

def decrypt(ciphertext):
    cipher = AES.new(key, AES.MODE_CTR)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

def encrypt_user(string):
    encoded = string.encode()
    result1 = hashlib.sha256(encoded)
    a = result1.hexdigest()
    b = bytes(a, 'utf-8')
    encryptor = PKCS1_OAEP.new(key_Public)
    encrypted = encryptor.encrypt(b)
    return encrypted


def decrypt_user(encrypted):
    decryptor = PKCS1_OAEP.new(key_Private)
    decrypted = decryptor.decrypt(encrypted)
    return decrypted

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
db.create_all()
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    passw = db.Column(db.String(100))


    def __init__(self, user, passw):
        self.user = user
        self.passw = passw

db.create_all()

def name(a):
    con = sqlite3.connect('Danhba.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT name FROM data ')
    all = cur.fetchall()
    alll = all[a]
    c = alll[0]
    decrypt_name = decrypt(c).decode()
    return decrypt_name


def email(a):
    con = sqlite3.connect('Danhba.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT email FROM data ')
    all = cur.fetchall()
    alll = all[a]
    c = alll[0]
    decrypt_email = decrypt(c).decode()
    return decrypt_email

def phone(a):
    con = sqlite3.connect('Danhba.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT phone FROM data ')
    all = cur.fetchall()
    alll = all[a]
    c = alll[0]
    decrypt_phone = decrypt(c).decode()
    return decrypt_phone

def SHA(userx):
    encoded = userx.encode()
    result2 = hashlib.sha256(encoded)
    a = result2.hexdigest()
    return a

#db.session.commit()
@app.route('/', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        con = sqlite3.connect('Danhba.sqlite3')
        cur = con.cursor()
        cur.execute('SELECT * FROM account ')
        all = cur.fetchall()
        alll = all[0]
        m = alll[1]
        a = decrypt_user(m)
        n = alll[2]
        b = decrypt_user(n)
        x = SHA(request.form['user'])
        xa = x.encode()
        y = SHA(request.form['password'])
        yb = y.encode()
        print(a)
        print(b)
        print(x)
        print(y)
        if(a==xa and b==yb):
            flash("Well done! You successfully logged in to this website")
            return redirect(url_for('Index'))
        else:
           flash("Incorrect username or password")
    return render_template("login.html")

@app.route('/Index')
def Index():
    all_data = Data.query.all()
    print(all_data)
    return render_template("index.html", peoples = all_data)
@app.route('/Register' , methods = ['GET', 'POST'])
def Register():
    if request.method == 'POST':
        if(request.form['password']== request.form['confirm_password']):
            user = Account(encrypt_user(request.form['user']) , encrypt_user(request.form['password']))
            db.session.add(user)
            db.session.commit()
            flash(" Registor successfully")
            return redirect(url_for('Login'))
        else:
            flash(" Error: Something went wrong. User Registration failed")
    return render_template("registration.html")


@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        danhsach = Data(encrypt(request.form['name']), encrypt(request.form['email']), encrypt(request.form['phone']))
        db.session.add(danhsach)
        db.session.commit()
        flash("Inserted Successfully")
        return redirect(url_for('Index'))
    return render_template("index.html")


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = encrypt(request.form['name'])
        my_data.email = encrypt(request.form['email'])
        my_data.phone = encrypt(request.form['phone'])
        db.session.commit()
        flash(my_data.name,my_data.email)

        return redirect(url_for('Index'))
    return render_template("index.html")


@app.route('/decrypt_data/<id>', methods=['GET', 'POST'])
def decrypt_data(id):
         a= int(id)
         flash(name(a-1))
         flash(email(a-1))
         flash(phone(a-1))
        # print(my_data)
         return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get_or_404(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('Index'))
@app.route('/log_out', methods=['GET', 'POST'])
def log_out():
    return render_template('login.html')
if __name__ == "__main__":
    app.run(debug=True)