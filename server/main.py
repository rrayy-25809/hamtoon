from flask import Flask, render_template

flask = Flask(__name__, template_folder='../dist', static_folder='../dist/assets')
flask.secret_key = 'LN$oaYB9-5KBT7G'

@flask.route("/")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    flask.run(debug=True, host='0.0.0.0')