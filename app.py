from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "idgafkltsic"

boggle_game = Boggle()

@app.route('/')
def show_home():
    """ Show Board """
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template("index.html", board=board, highscore=highscore, numplays=numplays)

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    session['numplays'] = numplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)