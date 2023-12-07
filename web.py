from flask import Flask, render_template, request, redirect, session

from stats_test import (
    search_player,
    choose_player,
    player_stats,
    match_stats,
    lobby_stats,
)

app = Flask(__name__)

nicknames_list = []


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route("/name/", methods=["GET", "POST"])
def find_name():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        search_player(nickname)

        # You might want to add the selected nickname to your nicknames_list here
        nicknames_list.append(nickname)

        # Redirect to the display page
        return redirect("/display_nicknames")

    return render_template("input_nickname.html")


@app.route("/display_nicknames")
def display_nicknames():
    return render_template("names.html", nicknames=nicknames_list)


if __name__ == "__main__":
    app.run(debug=True)
