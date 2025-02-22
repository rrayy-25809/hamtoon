from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

flask = Flask(__name__, template_folder='../dist', static_folder='../dist/assets')
conn = sqlite3.connect('server/db/user.db', check_same_thread=False)
cursor = conn.cursor()
flask.secret_key = 'LN$oaYB9-5KBT7G'

# SQLite 데이터베이스 초기화
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            "id" TEXT PRIMARY KEY,
            "password" TEXT,
            "nickname" TEXT,
            "bookmark" TEXT
        );
    ''')
    conn.commit()

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
        password = request.form["password"]
        cursor.execute("SELECT * FROM users WHERE id = ? AND password = ?", (user_id, password))
        user = cursor.fetchone()
        if user:
            session["user_id"] = user_id
            return redirect(url_for("main"))
        else:
            return "로그인 실패", 401
    return render_template("login.html")

@flask.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = request.form["id"]
        password = request.form["password"]
        nickname = request.form["nickname"]
        try:
            cursor.execute("INSERT INTO users (id, password, nickname) VALUES (?, ?, ?)", (user_id, password, nickname))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "이미 존재하는 아이디입니다.", 400
    return render_template("signup.html")

if __name__ == '__main__':
    init_db()
    flask.run(debug=True, host='0.0.0.0')