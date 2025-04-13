import requests
from bs4 import BeautifulSoup
import re
from match import Match

def get_current_matchday():
    url = "https://www.kicker.de/bundesliga/spieltag"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    current_matchday = "matchday not found"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        matchday_option = soup.find_all("option", selected=True)[1]  # Zweiter 'selected'
        if not matchday_option:
            raise Exception("Spieltag-Option nicht gefunden.")

        # Spieltag extrahieren
        spieltag_match = re.search(r"(\d+)\. Spieltag", matchday_option.text.strip())
        if not spieltag_match:
            raise Exception("Spieltag konnte nicht extrahiert werden.")

        current_matchday = int(spieltag_match.group(1))

    return current_matchday
           

def get_current_season():
    url = "https://www.kicker.de/bundesliga/spieltag"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    saison = 'saison not found'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        season_option = soup.find("option", selected=True)
        if not season_option:
            raise Exception("Saison-Option nicht gefunden.")

        # Saison extrahieren
        saison_full = season_option["value"].split("/")[-1]  # z.B. "2024-25"
        saison_kurz = saison_full[-5:]  # sichergehen: "24-25"
        saison = saison_kurz

    return saison

def scrape_kicker_prognose():
    url = "https://www.kicker.de/die-bundesliga-prognose-unsere-expertentipps-993443/artikel"

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
            tips.append({
                "date": "",
                "kickoff_time": "",
                "home_team": home_team, 
                "away_team": away_team,
                "match": title,
                "tip": tipp_text,
                "result": ""
            })

    return tips

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

                    # Nur rot markierte Tipps extrahieren
                    if 'color: red' in cells[7].get('style', ''):
                        tipps.append({
                            'home_team': home_team,
                            'away_team': away_team,
                            'tip': tip, 
                            'date': date,
                            'kickoff_time': kickoff_time,
                            'result': result
                        })

            # Ausgabe der Ergebnisse
            
        else:
            print("https://www.bundesliga-prognose.de nicht erreichbar")

    return tipps


def scrape_buli_tipphilfe_prognose():
    url = "https://www.buli-tipphilfe.de/"

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
        bundesliga_section = soup.find(id="pills-Bundesliga1")

        if bundesliga_section:
            # Wir holen alle sichtbaren Zeilen – die Struktur von oben nach unten
            rows = bundesliga_section.find_all("div", class_="row border-bottom", recursive=True)

            for row in rows:
                # Schritt 1: Begegnung finden
                match_div = row.find("div", string=lambda text: text and ":" in text)
                if not match_div:
                    continue

                match_text = match_div.get_text(strip=True)
                if ":" not in match_text:
                    continue

                heim, auswaerts = [t.strip() for t in match_text.split(":", 1)]

                # Schritt 2: TIPP suchen innerhalb des gleichen Blocks
                tipp = None
                all_divs = row.find_all("div")
                for i, div in enumerate(all_divs):
                    if div.get_text(strip=True).upper() == "TIPP":
                        if i + 1 < len(all_divs):
                            tipp = all_divs[i + 1].get_text(strip=True)
                            break

                tipps.append({
                    "heimteam": heim,
                    "auswaertsteam": auswaerts,
                    "tipp": tipp
                })

    return tipps

def scrape_sportwettenvergleich_prognose():
    url  = "https://www.sportwettenvergleich.net/kickform/bundesliga-spieltagstipps"

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
                    date = date_elem.text.strip() if date_elem else "Unbekanntes Datum"

                    left_team_elem = li.find("strong", class_="left")
                    left_team = left_team_elem.text.strip() if left_team_elem else "?"

                    right_team_elem = li.find("strong", class_="right")
                    right_team = right_team_elem.text.strip() if right_team_elem else "?"

                    score_elem = li.find("span", class_="score_sidebar played") or li.find("span", class_="score_sidebar")
                    score = score_elem.text.strip() if score_elem else "?"

                    match_str = f"{date}: {left_team} - {right_team} {score}"
                    tipps.append(match_str)

    return tipps

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
                teams = game.get_text(strip=True).replace(f"{game_number}. ", "")  # Die Teams (z.B. "VfL Wolfsburg - RB Leipzig")
                
                # Tipp extrahieren
                tip_strong = game.find_next('strong', text=lambda x: x and 'Tipp:' in x)
                if tip_strong:
                    tip = tip_strong.get_text(strip=True).replace('Tipp: ', '')  # Den Tipp extrahieren, z.B. "1-2"
                    
                    # Tipp und Spielpaarung speichern
                    tipps.append((teams, tip))

    return tipps

def create_match_objects_by_tip_list(tip_list):

    erste_bundesliga_teams=[
        "FC Bayern München", 
        "Bayer 04 Leverkusen",
        "Eintracht Frankfurt",
        "RB Leipzig",
        "1.FSV Mainz 05",
        "SC Freiburg",
        "Bor. Mönchengladbach",
        "Borussia Dortmund",
        "FC Augsburg",
        "VfB Stuttgart",
        "SV Werder Bremen",
        "VfL Wolfsburg",
        "1.FC Union Berlin",
        "TSG Hoffenheim",
        "FC St. Pauli",
        "1.FC Heidenheim",
        "VfL Bochum",
        "Holstein Kiel"
    ]

    match_objects = []

    for tip in tip_list:

        # if "" in tip["home_team"]:
        #     tip["home_team"] = ""
        # if "" in tip["away_team"]:
        #     tip["away_team"] = ""

        if "Augsburg" in tip["home_team"]:
            tip["home_team"] = "FC Augsburg"
        if "Augsburg" in tip["away_team"]:
            tip["away_team"] = "FC Augsburg"

        if "Bayern" in tip["home_team"]:
            tip["home_team"] = "FC Bayern München"
        if "Bayern" in tip["away_team"]:
            tip["away_team"] = "FC Bayern München"

        if "Bochum" in tip["home_team"]:
            tip["home_team"] = "VfL Bochum"
        if "Bochum" in tip["away_team"]:
            tip["away_team"] = "VfL Bochum"

        if "Bremen" in tip["home_team"]:
            tip["home_team"] = "SV Werder Bremen"
        if "Bremen" in tip["away_team"]:
            tip["away_team"] = "SV Werder Bremen"

        if "Dortmund" in tip["home_team"]:
            tip["home_team"] = "Borussia Dortmund"
        if "Dortmund" in tip["away_team"]:
            tip["away_team"] = "Borussia Dortmund"

        if "Frankfurt" in tip["home_team"]:
            tip["home_team"] = "Eintracht Frankfurt"
        if "Frankfurt" in tip["away_team"]:
            tip["away_team"] = "Eintracht Frankfurt"

        if "Freiburg" in tip["home_team"]:
            tip["home_team"] = "SC Freiburg"
        if "Freiburg" in tip["away_team"]:
            tip["away_team"] = "SC Freiburg"

        if "Gladbach" in tip["home_team"]:
            tip["home_team"] = "Bor. Mönchengladbach"
        if "Gladbach" in tip["away_team"]:
            tip["away_team"] = "Bor. Mönchengladbach"
        
        if "Heidenheim" in tip["home_team"]:
            tip["home_team"] = "1.FC Heidenheim"
        if "Heidenheim" in tip["away_team"]:
            tip["away_team"] = "1.FC Heidenheim"

        if "Hoffenheim" in tip["home_team"]:
            tip["home_team"] = "TSG Hoffenheim"
        if "Hoffenheim" in tip["away_team"]:
            tip["away_team"] = "TSG Hoffenheim"

        if "Kiel" in tip["home_team"]:
            tip["home_team"] = "Holstein Kiel"
        if "Kiel" in tip["away_team"]:
            tip["away_team"] = "Holstein Kiel"
        
        if "Leipzig" in tip["home_team"]:
            tip["home_team"] = "RB Leipzig"
        if "Leipzig" in tip["away_team"]:
            tip["away_team"] = "RB Leipzig"

        if "Leverkusen" in tip["home_team"]:
            tip["home_team"] = "Bayer 04 Leverkusen"
        if "Leverkusen" in tip["away_team"]:
            tip["away_team"] = "Bayer 04 Leverkusen"

        if "Mainz" in tip["home_team"]:
            tip["home_team"] = "1.FSV Mainz 05"
        if "Mainz" in tip["away_team"]:
            tip["away_team"] = "1.FSV Mainz 05"

        if "Pauli" in tip["home_team"]:
            tip["home_team"] = "FC St. Pauli"
        if "Pauli" in tip["away_team"]:
            tip["away_team"] = "FC St. Pauli"

        if "Stuttgart" in tip["home_team"]:
            tip["home_team"] = "VfB Stuttgart"
        if "Stuttgart" in tip["away_team"]:
            tip["away_team"] = "VfB Stuttgart"
        
        if "Union" in tip["home_team"]:
            tip["home_team"] = "1.FC Union Berlin"
        if "Union" in tip["away_team"]:
            tip["away_team"] = "1.FC Union Berlin"

        if "Wolfsburg" in tip["home_team"]:
            tip["home_team"] = "VfL Wolfsburg"
        if "Wolfsburg" in tip["away_team"]:
            tip["away_team"] = "VfL Wolfsburg"
     


        if tip["home_team"] not in erste_bundesliga_teams:
            print(f'Home Team not found: {tip["home_team"]}')
        if tip["away_team"] not in erste_bundesliga_teams:
            print(f'Away Team not found: {tip["away_team"]}')

        match = Match(tip["home_team"], tip["away_team"], tip["tip"], tip["date"], tip["kickoff_time"], tip["result"] )
        match_objects.append(match)

    return match_objects



if __name__ == "__main__":

    #matchday_and_season_short = get_current_matchday_and_season()
    current_saison = get_current_season()
    current_matchday = get_current_matchday()

    all_tipps = []

    bundesliga_tipps = scrape_bundesliga_prognose()    
    kicker_tipps = scrape_kicker_prognose()
    # buli_tipphilfe_tipps = scrape_buli_tipphilfe_prognose()
    # sportwettenvergleich_tipps = scrape_sportwettenvergleich_prognose()
    # ninety_min_tipps = scrape_ninety_min_prognose(current_matchday, current_saison)

    # all_tipps.append(kicker_tipps)
    # all_tipps.append(bundesliga_tipps)
    # all_tipps.append(buli_tipphilfe_tipps)   
    # all_tipps.append(sportwettenvergleich_tipps)
    # all_tipps.append(ninety_min_tipps)

    A_bundesliga_tip_objects = create_match_objects_by_tip_list(bundesliga_tipps)
    B_kicker_tip_objects = create_match_objects_by_tip_list(kicker_tipps)

    print("done.")
    
