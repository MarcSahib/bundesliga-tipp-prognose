import requests
from bs4 import BeautifulSoup


def scrape_ninety_min_prognose(current_matchday, current_saison):
    
    url  = f"https://www.90min.de/bundesliga-prognose-vorhersage-tipps-zum-{current_matchday}-spieltag-{current_saison}"

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
        # Alle Spiele und Tipps durchgehen
        for game in soup.find_all('h2', class_='tagStyle_1igopqi-o_O-style_48hmcm-o_O-titleStyle_k8egye'):
            # Spielpaarung finden (z.B. "VfL Wolfsburg - RB Leipzig")
            teams_span = game.find('span', class_='tagStyle_z4kqwb-o_O-numberStyle_bdr0ip-o_O-tagStyle_1igopqi')
            if teams_span:
                game_number = teams_span.get_text(strip=True).replace('.', '')  # Spielnummer (1, 2, 3,...)
                teams_raw = game.get_text(strip=True).replace(f"{game_number}. ", "")  # Die Teams (z.B. "VfL Wolfsburg - RB Leipzig")
                teams = teams_raw.replace(f"{game_number}.","")
                parts = teams.split("-")
                if len(parts) !=2:
                    raise ValueError("Ungültiges Format. Erwartet wird 'TeamA - TeamB'")
                home_team = parts[0].strip()
                away_team = parts[1].strip()

                # Tipp extrahieren
                tip_strong = game.find_next('strong', text=lambda x: x and 'Tipp:' in x)
                if tip_strong:
                    tip_raw = tip_strong.get_text(strip=True).replace('Tipp: ', '')  # Den Tipp extrahieren, z.B. "1-2"
                    tip = tip_raw.replace("-",":")
                    home_goals_tip, away_goals_tip = tip.split(":")
                    # Tipp und Spielpaarung speichern
                    tipps.append({
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_goals_tip": home_goals_tip, 
                        "away_goals_tip": away_goals_tip,
                        "tip": tip, # Wird auf sportwettenvwergleich.net auf das tatsächliche Ergebnis aktualisiert!
                        "date": "",
                        "kickoff_time": "",
                        "result": ""

                    })

    return tipps