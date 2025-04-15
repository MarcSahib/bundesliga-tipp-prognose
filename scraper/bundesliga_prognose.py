import requests
from bs4 import BeautifulSoup


def scrape_bundesliga_prognose():
   
    url = "https://www.bundesliga-prognose.de/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }

    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tipps = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Suche das th mit data-field="platz"
        th_tag = soup.find('th', {'data-field': 'platz'})

        if th_tag:
            # Zum <table> Element hochgehen
            table = th_tag.find_parent('table')

            # <tbody> finden
            tbody = table.find('tbody')

            # Durch alle <tr> im <tbody>
            for row in tbody.find_all('tr'):
                cells = row.find_all('td')

                if len(cells) >= 6:
                    date = cells[0].get_text(strip=True)
                    kickoff_time = cells[1].get_text(strip=True)
                    home_team = cells[2].get_text(strip=True)
                    heimtea_short_name = cells[3].get_text(strip=True)
                    away_team = cells[4].get_text(strip=True).lstrip("- ").strip()
                    auswärtsteam_short_name = cells[5].get_text(strip=True)                                    
                    result = cells[6].get_text(strip=True)
                    tip = cells[7].get_text(strip=True)
                    home_goals_tip, away_goals_tip = tip.split(":")

                    # Nur rot markierte Tipps extrahieren
                    if 'color: red' in cells[7].get('style', ''):
                        tipps.append({
                            'home_team': home_team,
                            'away_team': away_team,
                            'home_goals_tip': home_goals_tip,
                            'away_goals_tip': away_goals_tip,
                            'tip': tip, 
                            'date': date,
                            'kickoff_time': kickoff_time,
                            'result': result
                        })

            # Ausgabe der Ergebnisse
            
        else:
            print("https://www.bundesliga-prognose.de nicht erreichbar")

    return tipps