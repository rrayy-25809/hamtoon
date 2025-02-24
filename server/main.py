from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from db_manager import db_manager
import api_request

flask = Flask(__name__, template_folder='../dist', static_folder='../dist/assets')
flask.secret_key = 'LN$oaYB9-5KBT7G'
db = db_manager(sqlite3.connect('server/db/user.db', check_same_thread=False))

@flask.route("/")
def main():
    return render_template("index.html")

@flask.route("/mypage")
def mypage():
    return render_template("mypage.html")

@flask.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["id"]
        if db.login(user_id, request.form["password"]):
            session["user_id"] = user_id
            return redirect(url_for("main"))
        else:
            return "로그인 실패", 401
    return render_template("login.html")

@flask.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if db.signup(request.form["id"], request.form["password"], request.form["nickname"]):
            return redirect(url_for("login"))
        else:
            return "이미 존재하는 아이디입니다.", 400
    return render_template("signup.html")

@flask.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main"))

if __name__ == '__main__':
    db_manager.init_db()
    flask.run(debug=True, host='0.0.0.0')