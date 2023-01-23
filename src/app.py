import requests
import pandas
import logging
import json
from datetime import datetime
from collections import defaultdict
import openpyxl
from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('index1'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/index')
@login_required
def index1():
    return render_template('index.html')

@app.route('/olt-foxcom')
@login_required
def oltfoxcom():
    return render_template('oltfoxcom.html')

@app.route('/olt-huawei-zte')
@login_required
def olthz():
    return render_template('olthz.html')

@app.route('/result',methods=['POST', 'GET'])
@login_required
def result():
    output = request.form.to_dict()
    pon_r = output["pon"]
   # print(output)
   # pon = output["pon"]
    url = "https://tvpacifico.smartolt.com/api/onu/get_onu_catv_status/"
    logging.basicConfig(level=logging.DEBUG,filename="mylog.log",format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    payload={}
    files={}
    headers = {
      'X-Token': '4a3d5f9b0edd4857b799417717c5c5b2'
    }
    pon = requests.request("GET", url + str(pon_r), headers=headers, data=payload, files=files)
    ponjson = pon.json()
    logging.info(pon.text)
    if str(ponjson["status"]) == 'true':

        return render_template('olthz.html', pon = "La ONT " + str(pon_r) + " tiene CATV " + ponjson["onu_catv_status"])
    else:
        return render_template('olthz.html', pon = "La ONT " + str(pon_r) + " no se ecuentra en la OLT")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(host="0.0.0.0")
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
