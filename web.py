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
# matches_data = []


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
            # print("data:", data)
            processed_data = choose_player(data)
            # print("procssed_data:", processed_data)
            players = processed_data
    # print("final players:", players)
    return render_template("names.html", players_data=players, players=players)


@app.route("/stats", methods=["GET", "POST"])
def last_matches():
    matches_data = []

    if request.method == "POST":
        items = request.form.getlist("items")
        print(items)
        if items:
            player_id = items[0].get("stats", {}).get("Player Id")
            print("player id:", player_id)

            if player_id:
                url = f"https://open.faceit.com/data/v4/players/{player_id}/games/cs2/stats"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {FACEIT_KEY}",
                }
                limit = 10
                params = {"offset": 0, "limit": limit}

                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    player_data = player_stats(player_id, limit)
                    print(player_data)
                    processed_data = match_stats(player_data)
                    print(processed_data)
                    matches_data = processed_data if processed_data else []

    return render_template("matches.html", matches_data=matches_data)




if __name__ == "__main__":
    app.run(debug=True)
