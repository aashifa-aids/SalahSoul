from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(_name_)
app.secret_key = "replace_this_with_a_random_secret"  # change this for real projects

# Demo prayer list (order)
PRAYERS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

QUOTES = [
    "Salah is the key to success 🌙",
    "Don’t miss your connection with Allah 💫",
    "Peace begins on your prayer mat 🕋",
    "Prayer is better than sleep 🌅",
    "Each Salah brings you closer to Jannah ✨",
    "The coolness of the believer’s eyes is in Salah 💖"
]

def init_session():
    """Initialize session values if missing"""
    if "index" not in session:
        session["index"] = 0           # which prayer we're on (0..4)
    if "prayed_count" not in session:
        session["prayed_count"] = 0   # how many yes responses

@app.route("/", methods=["GET"])
def home():
    init_session()
    idx = session["index"]
    # if user completed all 5, show summary screen
    if idx >= len(PRAYERS):
        prayed = session.get("prayed_count", 0)
        # prepare summary message
        if prayed == 5:
            final_msg = "🌙 MashaAllah! You completed all prayers today."
        elif prayed >= 3:
            final_msg = "💫 Good effort! Try to complete all next time — consistency is key."
        elif prayed >= 1:
            final_msg = "✨ You started well! Every step toward Allah counts."
        else:
            final_msg = "💭 Don't give up. Tomorrow is a new chance to reconnect with Allah."
        return render_template("index.html", finished=True, prayed=prayed, final_msg=final_msg)

    # otherwise show current prayer
    current_prayer = PRAYERS[idx]
    return render_template("index.html", finished=False, prayer=current_prayer, prayed=session.get("prayed_count", 0))

@app.route("/response", methods=["POST"])
def response():
    init_session()
    ans = request.form.get("answer")
    if ans == "yes":
        session["prayed_count"] = session.get("prayed_count", 0) + 1
        message = "💖 Alhamdulillah! May Allah accept your Salah."
    else:
        message = "💭 " + random.choice(QUOTES)

    # advance to next prayer
    session["index"] = session.get("index", 0) + 1

    # pass the message to next page via query param (or you could store in session)
    return redirect(url_for("show_message", msg=message))

@app.route("/message")
def show_message():
    # show the message then redirect to home (so user sees it)
    msg = request.args.get("msg", "")
    # render home page but with a flash-like message (we'll display it in template)
    init_session()
    idx = session.get("index", 0)
    # if all done, go to home which shows summary
    if idx >= len(PRAYERS):
        return redirect(url_for("home"))
    current_prayer = PRAYERS[idx] if idx < len(PRAYERS) else None
    return render_template("index.html", finished=False, prayer=current_prayer, message=msg, prayed=session.get("prayed_count", 0))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

if _name_ == "_main_":
    app.run(debug=True)
