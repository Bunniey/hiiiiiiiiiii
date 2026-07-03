from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = "lavanya_secret_key"

DATABASE = "database/responses.db"


def init_db():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nickname TEXT,

        normal_food TEXT,

        special_food TEXT,

        forever_food TEXT,

        foodie_type TEXT,

        foodie_note TEXT,

        flower TEXT,

        genre TEXT,

        artist TEXT,

        spotify TEXT,

        drink TEXT,

        hobbies TEXT,

        hobby_other TEXT,

        scroll_content TEXT,

        feedback TEXT,

        feedback_note TEXT

        )
    """)

    conn.commit()

    conn.close()


init_db()


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/nickname", methods=["GET","POST"])
def nickname():

    if request.method=="POST":

        session["nickname"]=request.form["nickname"]

        return redirect(url_for("page3"))

    return render_template("nickname.html")


@app.route("/page3")
def page3():

    return render_template(
        "page3.html",
        nickname=session.get("nickname")
    )


@app.route("/page4")
def page4():

    return render_template(
        "page4.html",
        nickname=session.get("nickname")
    )


@app.route("/food1",methods=["GET","POST"])
def food1():

    if request.method=="POST":

        session["normal_food"]=request.form["normal_food"]

        session["special_food"]=request.form["special_food"]

        return redirect(url_for("food2"))

    return render_template("food1.html")


@app.route("/food2",methods=["GET","POST"])
def food2():

    if request.method=="POST":

        session["forever_food"]=request.form["forever_food"]

        return redirect(url_for("foodie"))

    return render_template("food2.html")


@app.route("/foodie",methods=["GET","POST"])
def foodie():

    if request.method=="POST":

        session["foodie_type"]=request.form["foodie_type"]

        session["foodie_note"]=request.form["foodie_note"]

        return redirect(url_for("flowers"))

    return render_template("foodie.html")


@app.route("/flowers",methods=["GET","POST"])
def flowers():

    if request.method=="POST":

        session["flower"]=request.form["flower"]

        return redirect(url_for("music"))

    return render_template("flowers.html")


@app.route("/music",methods=["GET","POST"])
def music():

    if request.method=="POST":

        session["genre"]=request.form["genre"]

        return redirect(url_for("artist"))

    return render_template("music.html")


@app.route("/artist",methods=["GET","POST"])
def artist():

    if request.method=="POST":

        session["artist"]=request.form["artist"]

        session["spotify"]=request.form["spotify"]

        return redirect(url_for("beverage"))

    return render_template("artist.html")


@app.route("/beverage",methods=["GET","POST"])
def beverage():

    if request.method=="POST":

        session["drink"]=request.form["drink"]

        return redirect(url_for("hobbies"))

    return render_template("beverage.html")


@app.route("/hobbies",methods=["GET","POST"])
def hobbies():

    if request.method=="POST":

        session["hobbies"]=json.dumps(request.form.getlist("hobbies"))

        session["other"]=request.form["other"]

        return redirect(url_for("scroll"))

    return render_template("hobbies.html")


@app.route("/scroll",methods=["GET","POST"])
def scroll():

    if request.method=="POST":

        session["scroll"]=request.form["scroll"]

        return redirect(url_for("thankyou"))

    return render_template("scroll.html")


@app.route("/thankyou")
def thankyou():

    return render_template("thankyou.html")


@app.route("/feedback",methods=["GET","POST"])
def feedback():

    if request.method=="POST":

        session["feedback"]=request.form["feedback"]

        session["feedback_note"]=request.form["feedback_note"]

        conn=sqlite3.connect(DATABASE)

        cur=conn.cursor()

        cur.execute("""

        INSERT INTO responses(

        nickname,

        normal_food,

        special_food,

        forever_food,

        foodie_type,

        foodie_note,

        flower,

        genre,

        artist,

        spotify,

        drink,

        hobbies,

        hobby_other,

        scroll_content,

        feedback,

        feedback_note

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        session.get("nickname"),

        session.get("normal_food"),

        session.get("special_food"),

        session.get("forever_food"),

        session.get("foodie_type"),

        session.get("foodie_note"),

        session.get("flower"),

        session.get("genre"),

        session.get("artist"),

        session.get("spotify"),

        session.get("drink"),

        session.get("hobbies"),

        session.get("other"),

        session.get("scroll"),

        session.get("feedback"),

        session.get("feedback_note")

        ))

        conn.commit()

        conn.close()

        return redirect(url_for("goodbye"))

    return render_template("feedback.html")


@app.route("/goodbye")
def goodbye():
    return render_template("goodbye.html")


if __name__=="__main__":
    app.run(debug=True)
