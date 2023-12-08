from config import FACEIT_KEY
from tabulate import tabulate
import requests


def search_player(nickname):
    # nickname = input("Search for a nickname: ")
    url = f"https://open.faceit.com/data/v4/search/players?nickname={nickname}&offset=0&limit=20"
    headers = {"accept": "application/json", "Authorization": f"Bearer {FACEIT_KEY}"}
    params = {"offset": 0, "limit": 20}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        choose_player(data)
        selected_player = player_choice(data)
        return selected_player
    else:
        print(f"Error: {response.status_code}, {response.text}")


def process_selected_player(selected_player):
    if selected_player:
        nickname, player_id = selected_player
        print(f"Selected player: {nickname} (Player ID: {player_id})")
        limit = int(
            input(
                "Enter the number of match statistics you would like to see (e.g., Last 5 Matches): "
            )
        )
        matches_data = player_stats(player_id, limit)
        if matches_data:
            match_stats_data = match_stats(matches_data)
            return {
                "nickname": nickname,
                "player_id": player_id,
                "matches_data": match_stats_data,
            }
        else:
            print("No match statistics found.")
    else:
        print("No player selected.")
        return None


def choose_player(data):
    items = data.get("items", [])
    if not items:
        print("No players found.")
        return None

    players_data = []
    for index, player in enumerate(items, start=1):
        if not isinstance(player, dict):
            print(f"Error: Player at index {index} is not a dictionary.")
            continue

        nickname = player.get("nickname", "N/A")
        player_id = player.get("player_id", "N/A")
        players_data.append(
            {"index": index, "nickname": nickname, "player_id": player_id}
        )
    return players_data


def player_choice(data):
    items = data.get("items", [])
    while True:
        try:
            choice = int(input("Choose a player number (1-{}): ".format(len(items))))
            if 1 <= choice <= len(items):
                selected_player = items[choice - 1]
                nickname = selected_player.get("nickname", "N/A")
                player_id = selected_player.get("player_id", "N/A")
                return nickname, player_id
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def player_stats(player_id, limit):
    url = f"https://open.faceit.com/data/v4/players/{player_id}/games/cs2/stats"
    headers = {"accept": "application/json", "Authorization": f"Bearer {FACEIT_KEY}"}
    params = {"offset": 0, "limit": limit}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        return data  # Return the match statistics data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def match_stats(data):
    matches = data.get("items", [])
    matches_data = []

    if not matches:
        print("No match statistics found.")
        return matches_data

    headers = [
        "Map",
        "Result",
        "Score",
        "K/D Ratio",
        "Kills",
        "Assists",
        "Deaths",
        "Headshot %",
    ]

    for index, match in enumerate(matches, start=1):
        stats = match.get("stats", {})
        cs_map = stats.get("Map", "N/A")[3:].capitalize()
        result = stats.get("Result", "N/A")
        if result == "0":
            result = "Loss"
        else:
            result = "Win"
        score = stats.get("Score", "N/A")
        k_d_ratio = stats.get("K/D Ratio", "N/A")
        kills = stats.get("Kills", "N/A")
        assists = stats.get("Assists", "N/A")
        deaths = stats.get("Deaths", "N/A")
        headshot_perc = stats.get("Headshots %", "N/A")

        matches_data.append(
            [
                cs_map,
                result,
                score,
                k_d_ratio,
                kills,
                assists,
                deaths,
                f"{headshot_perc}%",
            ]
        )

    return {"headers": headers, "matches_data": matches_data}


def lobby_stats(match_id):
    url = f"https://open.faceit.com/data/v4/matches/{match_id}/stats"
    headers = {"accept": "application/json", "Authorization": f"Bearer {FACEIT_KEY}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        cs_map = (
            data.get("rounds", [])[0]
            .get("round_stats", {})
            .get("Map", "N/A")[3:]
            .capitalize()
        )
        score = data.get("rounds", [])[0].get("round_stats", {}).get("Score", "N/A")

        print(f"Map: {cs_map} | Score: {score}")

        rounds = data.get("rounds", [])

        for round_info in rounds:
            teams = round_info.get("teams", [])

            for team in teams:
                team_name = team.get("team_stats", {}).get("Team", "N/A")
                team_score = team.get("team_stats", {}).get("Final Score", "N/A")
                team_result = (
                    "Win"
                    if team.get("team_stats", {}).get("Team Win", "0") == "1"
                    else "Loss"
                )

                print(
                    f"\nTeam: {team_name} | Score: {team_score} | Result: {team_result}"
                )

                players = team.get("players", [])
                player_data = []

                for player in players:
                    player_name = player.get("nickname", "N/A")
                    k_d_ratio = player.get("player_stats", {}).get("K/D Ratio", "N/A")
                    kills = player.get("player_stats", {}).get("Kills", "N/A")
                    assists = player.get("player_stats", {}).get("Assists", "Ns/A")
                    deaths = player.get("player_stats", {}).get("Deaths", "N/A")
                    headshot_perc = player.get("player_stats", {}).get(
                        "Headshots %", "N/A"
                    )

                    player_data.append(
                        [
                            player_name,
                            k_d_ratio,
                            kills,
                            assists,
                            deaths,
                            f"{headshot_perc}%",
                        ]
                    )

                headers = [
                    "Player",
                    "K/D Ratio",
                    "Kills",
                    "Assists",
                    "Deaths",
                    "Headshot %",
                ]
                print(
                    tabulate(
                        player_data,
                        headers=headers,
                        tablefmt="fancy_grid",
                        stralign="right",
                    )
                )
    else:
        print(f"Error: {response.status_code}, {response.text}")


def choose_match(matches_data):
    matches = matches_data.get("items", [])

    if not matches:
        print("No match statistics found.")
        return

    while True:
        try:
            choice = int(input("Choose a match number (1-{}): ".format(len(matches))))
            if 1 <= choice <= len(matches):
                selected_match = matches[choice - 1]
                match_id = selected_match.get("stats", {}).get("Match Id", "N/A")
                lobby_stats(match_id)
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """
    Runs the function search_player()
    """
    nickname = input("Enter a username: ")
    selected_player = search_player(nickname)
    print(process_selected_player(selected_player))


if __name__ == "__main__":
    main()
