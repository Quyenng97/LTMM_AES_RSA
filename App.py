from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import pyaes
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Danhba.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

key_r = get_random_bytes(22)
key = b64encode(key_r)
#key = b'cdhtdvdfracdcdhtdvdfracddfrthvfe'
def encrypt(plaintext):
    ciphertext = pyaes.AESModeOfOperationCTR(key).encrypt(plaintext)
    return ciphertext

def decrypt(ciphertext):
    plaintext = pyaes.AESModeOfOperationCTR(key).decrypt(ciphertext)
 #   print(plaintext)
  #  return plaintext.decode()
    return plaintext

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
    c= alll[0]
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
#a= name(1)
#print(a)
#con.close()
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("DanhBa.html", peoples = all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        danhsach = Data(encrypt(request.form['name']), encrypt(request.form['email']), encrypt(request.form['phone']))
        db.session.add(danhsach)
        db.session.commit()
        flash("Inserted Successfully")
        return redirect(url_for('Index'))
    return render_template("DanhBa.html")

# this is our update route where we are going to update our employee
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
    return render_template("DanhBa.html")


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

if __name__ == "__main__":
    app.run(debug=True)