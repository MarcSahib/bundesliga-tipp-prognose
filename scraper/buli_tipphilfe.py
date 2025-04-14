import requests
from bs4 import BeautifulSoup


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
                    "home_team": heim,
                    "away_team": auswaerts,
                    "tip": tipp,
                    "date": "",
                    "kickoff_time": "",
                    "result": ""

                })

    return tipps