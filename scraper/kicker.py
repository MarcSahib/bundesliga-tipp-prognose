import requests
from bs4 import BeautifulSoup


def scrape_kicker_prognose():
    
    url = "https://www.kicker.de/die-bundesliga-prognose-unsere-expertentipps-993443/artikel" # hat scheinbar keine eindeutige URL für Spieltag + saison

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    all_h2 = soup.find_all("h2")
    tips = []

    for h2 in all_h2:
        h2_text = h2.get_text(strip=True)

        # h2 mit bestimmter Klasse ausschließen
        if "kick__site-headline" in h2.get("class", []):
            continue

        # exakten Text ausschließen
        if h2_text == "Die Bundesliga-Prognose: Unsere Expertentipps":
            continue

        title = h2.get_text(strip=True)
        if "vs." in title:
            parts = title.split("vs.")
            home_team = parts[0].strip()
            away_team = parts[1].strip()

        next_strong = h2.find_next("strong")
        if next_strong and "Unser Tipp:" in next_strong.get_text():
            tipp_text = next_strong.get_text(strip=True).replace("Unser Tipp:", "").strip()
            home_goals_tip, away_goals_tip = tipp_text.split(":")
            tips.append({
                "date": "",
                "kickoff_time": "",
                "home_team": home_team, 
                "away_team": away_team,
                "home_goals_tip": home_goals_tip,
                "away_goals_tip": away_goals_tip,
                "match": title,
                "tip": tipp_text,
                "result": ""
            })

    return tips