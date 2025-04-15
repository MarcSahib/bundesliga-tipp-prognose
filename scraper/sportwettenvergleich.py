import requests
from bs4 import BeautifulSoup


def scrape_sportwettenvergleich_prognose():
    
    url  = "https://www.sportwettenvergleich.net/kickform/bundesliga-spieltagstipps" # besitzt /30/ -> /<Spieltag>/

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    tipps = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Alle divs mit class 'matchday' holen
        matchday_divs = soup.find_all("div", class_="matchday")

        for div in matchday_divs:
            # Sicherstellen, dass es sich **nicht** um das <section> handelt
            if div.name != "section":
                ul = div.find("ul")
                if not ul:
                    continue

                for li in ul.find_all("li"):
                    date_elem = li.find("small")
                    date_time = date_elem.text.strip() if date_elem else "Unbekanntes Datum"
                    cleaned_date = date_time.replace("Uhr", "").strip()
                    date, kickoff_time = cleaned_date.split(" ")

                    #if date != "Unbekanntes Datum":
                        

                    left_team_elem = li.find("strong", class_="left")
                    left_team = left_team_elem.text.strip() if left_team_elem else "?"

                    right_team_elem = li.find("strong", class_="right")
                    right_team = right_team_elem.text.strip() if right_team_elem else "?"

                    score_elem = li.find("span", class_="score_sidebar played") or li.find("span", class_="score_sidebar")
                    score_raw = score_elem.text.strip() if score_elem else "?"
                    score = score_raw.replace(" ","").strip()
                    home_goals_tip, away_goals_tip = score.split(":")
                    tipps.append({
                        "home_team": left_team,
                        "away_team": right_team,
                        "home_goals_tip": home_goals_tip,
                        "away_goals_tip": away_goals_tip,
                        "tip": score, # Wird auf sportwettenvwergleich.net auf das tatsächliche Ergebnis aktualisiert!
                        "date": date,
                        "kickoff_time": kickoff_time,
                        "result": ""

                    })

    return tipps