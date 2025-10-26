from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import duckdb
from flask_bcrypt import Bcrypt
from server.db_manager import db_manager
import server.api_request as api
import os
from dotenv import load_dotenv

load_dotenv()
flask = Flask(__name__, template_folder='../dist/client', static_folder='../dist/assets')
flask.secret_key = os.getenv("FLASK_KEY")
bcrypt = Bcrypt(flask)
db = db_manager(duckdb.connect('server/db/user.db'))
# db.init_db()

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
        password:str = request.form["password"] # type: ignore

        if bcrypt.check_password_hash(db.get_password_hash(user_id), password):
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
        user_id = request.form["id"]
        password:str = request.form["password"] # type: ignore

        if db.signup(user_id, bcrypt.generate_password_hash(password), request.form["nickname"]):
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
    webtoon = api.fetch_webtoon_detail(webtoon_id)
    
    webtoon_data = {
        **webtoon, # type: ignore
        'id': webtoon_id
    }
    
    return render_template("webtoon.html", **webtoon_data)

@flask.route("/today", methods=["POST"])
def today():
    return jsonify(api.fetch_today_webtoon())

@flask.route("/bookmark", methods=["POST"])
def bookmark():
    user_info = db.get_user_info(session["user_id"])
    bookmark = user_info[3]
    bookmark_list = []
    if bookmark:
        for i in bookmark.split(","):
            bookmark_list.append(api.fetch_webtoon_detail(i))
    return jsonify(bookmark_list)

@flask.route("/add_bookmark", methods=["POST"])
def add_bookmark():
    try:
        user_info = db.get_user_info(session["user_id"])
        bookmark = user_info[3] if user_info else ""
        bookmark_list = bookmark.split(",") if bookmark else []
        if not request.form["webtoon_id"] in bookmark_list:
            db.add_bookmark(session["user_id"], request.form["webtoon_id"]) # type: ignore
            return "added", 200
        else:
            db.remove_bookmark(session["user_id"], request.form["webtoon_id"]) # type: ignore
            return "removed", 200
    except KeyError:
        return "로그인이 필요합니다.", 401
    except Exception as e:
        return str(e), 500
    
@flask.route("/episode", methods=["POST"])
def episode():
    return jsonify(api.fetch_webtoon_episode(request.form["webtoon_id"]))

@flask.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response