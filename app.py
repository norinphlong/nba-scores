from flask import Flask, render_template, jsonify
from nba_api.live.nba.endpoints import scoreboard
import pytz
from datetime import datetime

app = Flask(__name__)

team_logos = {
    "Hawks": "https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg",
    "Celtics": "https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg",
    "Nets": "https://upload.wikimedia.org/wikipedia/en/4/44/Brooklyn_Nets_newlogo.svg",
    "Hornets": "https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg",
    "Bulls": "https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg",
    "Cavaliers": "https://upload.wikimedia.org/wikipedia/en/4/4b/Cleveland_Cavaliers_logo.svg",
    "Mavericks": "https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg",
    "Nuggets": "https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg",
    "Pistons": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Detroit_Pistons_logo.svg",
    "Warriors": "https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg",
    "Rockets": "https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg",
    "Pacers": "https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg",
    "Clippers": "https://upload.wikimedia.org/wikipedia/en/b/bb/Los_Angeles_Clippers_%282015%29.svg",
    "Lakers": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg",
    "Grizzlies": "https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg",
    "Heat": "https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg",
    "Bucks": "https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg",
    "Timberwolves": "https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg",
    "Pelicans": "https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg",
    "Knicks": "https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg",
    "Thunder": "https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg",
    "Magic": "https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg",
    "76ers": "https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg",
    "Suns": "https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg",
    "Trail Blazers": "https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg",
    "Kings": "https://upload.wikimedia.org/wikipedia/en/c/c7/Sacramento_Kings_logo.svg",
    "Spurs": "https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg",
    "Raptors": "https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg",
    "Jazz": "https://upload.wikimedia.org/wikipedia/en/f/f7/Utah_Jazz_primary_logo_2022.svg",
    "Wizards": "https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg"
}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scores")
def scores():
    try:
        board = scoreboard.ScoreBoard()
        games = board.get_dict()["scoreboard"]["games"]
        result = []
        for game in games:
            home_team = game["homeTeam"]["teamName"]
            away_team = game["awayTeam"]["teamName"]
            status_num = game["gameStatus"]  # 1 = upcoming, 2 = live, 3 = finished

            if status_num == 1:
                score_display = "Upcoming"
            elif status_num == 2:
                score_display = f"{game['awayTeam']['score']} - {game['homeTeam']['score']} (Live)"
            elif status_num == 3:
                score_display = f"{game['awayTeam']['score']} - {game['homeTeam']['score']} (Final)"
            else:
                score_display = "N/A"

            # Converting to user's local time
            utc_time = datetime.strptime(game["gameTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
            eastern = pytz.timezone("US/Eastern")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(eastern)
            time_str = local_time.strftime("%I:%M %p %Z")

            result.append({
                "home": home_team,
                "away": away_team,
                "score": score_display,
                "home_logo": team_logos.get(home_team, ""),
                "away_logo": team_logos.get(away_team, ""),
                "time": time_str,
                "status": status_num
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
