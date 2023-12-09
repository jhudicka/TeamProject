from flask import Flask, render_template, request, redirect, session

from stats import (
    search_player,
    process_selected_player,
    choose_player,
    player_stats,
    match_stats,
    requests,
    FACEIT_KEY,
)

app = Flask(__name__)

nicknames_list = []
players_data = []
# matches_data = []


@app.route("/")
def hello():
    """
    The first page the user sees when using the website, prompting the user to input their nickname.
    """
    return render_template("hello.html")


@app.route("/nicknames", methods=["GET", "POST"])
def display_nicknames():
    """
    Displays all of the associated nicknames based off of the user's input on the first page.
    """
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


@app.route("/stats", methods=["POST"])
def last_matches():
    """
    Displays the selected nicknames' match history from their last 10 games, showing information such as the day played, map, result, score, etc.
    """
    player_id = request.form.get("player_id")
    player_data = []
    matches_data = []

    if player_id:
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
                player_data = player_stats(player_id, limit)
                matches_data = match_stats(player_data)

        if not matches_data:
            print("No match statistics found.")
    print(matches_data)
    return render_template("matches.html", matches_data=matches_data)


if __name__ == "__main__":
    app.run(debug=True)
