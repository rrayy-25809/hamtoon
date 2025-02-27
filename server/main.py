from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from server.db_manager import db_manager
import server.api_request as api

flask = Flask(__name__, template_folder='../dist/client', static_folder='../dist/assets')
flask.secret_key = 'LN$oaYB9-5KBT7G'
db = db_manager(sqlite3.connect('server/db/user.db', check_same_thread=False))

@flask.route("/")
def main():
    return render_template("index.html")

@flask.route("/mypage")
def mypage():
    try:
        info = db.get_user_info(session["user_id"])
        return render_template("mypage.html", name = info[2])
    except KeyError:
        return "로그인이 필요합니다.", 401

@flask.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["id"]
        if db.login(user_id, request.form["password"]):
            session["user_id"] = user_id
            return redirect(url_for("main"))
        else:
            return "로그인 실패", 401
    elif "user_id" in session:
        return "이미 로그인되어 있습니다.", 400
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

@flask.route("/delete_acc")
def delete_acc():
    db.delete_acc(session["user_id"])
    session.pop("user_id", None)
    return redirect(url_for("main"))

@flask.route("/webtoon/<int:webtoon_id>")
def webtoon_id(webtoon_id):
    # Get webtoon details from API
    webtoon = api.fetch_webtoon_detail(webtoon_id)
    
    # Extract required information
    webtoon_data = {
        'title': webtoon['title'],
        'description': webtoon['about'],
        'thumbnail': webtoon['thumb'],
        'genre': webtoon['genre'],
        'age': webtoon['age'],
        'id': webtoon_id
    }
    
    return render_template("webtoon.html", **webtoon_data)

@flask.route("/today", methods=["POST"])
def today():
    return jsonify(api.fetch_today_webtoon())

@flask.route("/bookmark", methods=["POST"])
def bookmark():
    bookmark = db.get_user_info(session["user_id"])[3]
    # for i in bookmark:
    #     api.fetch_webtoon_detail(i)
    #     
    return jsonify(api.fetch_today_webtoon())

@flask.route("/add_bookmark", methods=["POST"])
def add_bookmark():
    db.add_bookmark(session["user_id"], request.form["webtoon_id"])
    return "OK"

@flask.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response