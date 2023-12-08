from flask import Flask, render_template, request, redirect, session

from stats_test import (
    search_player,
    process_selected_player,
    choose_player,
    player_stats,
    match_stats,
    lobby_stats,
    requests,
    FACEIT_KEY,
)

app = Flask(__name__)

nicknames_list = []
players_data = []


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route("/nicknames", methods=["GET", "POST"])
def display_nicknames():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        url = f"https://open.faceit.com/data/v4/search/players?nickname={nickname}&offset=0&limit=20"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {FACEIT_KEY}",
        }
        params = {"offset": 0, "limit": 20}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            processed_data = choose_player(data)
            players = processed_data
    return render_template("names.html", players_data=players, players=players)


@app.route("/stats", methods=["GET", "POST"])
def last_matches():
    if request.method == "POST":
        player_id = request.form.get("player")
        url = f"https://open.faceit.com/data/v4/players/{player_id}/games/cs2/stats"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {FACEIT_KEY}",
        }
        limit = 10

        params = {"offset": 0, "limit": limit}

        response = requests.get(url, headers=headers, params=params)

        # player_data = player_stats(player_id, limit)

        # if player_data:
        #     processed_data = match_stats(player_data)
        #     return render_template("matches.html", player_data=processed_data)
        if response.status_code == 200:
            data = response.json()
            player_data = player_stats(player_id, limit)
            processed_data = match_stats(player_data)
    return render_template("matches.html", player_data=processed_data)


if __name__ == "__main__":
    app.run(debug=True)
