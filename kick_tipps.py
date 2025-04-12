import requests
from bs4 import BeautifulSoup


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
        next_strong = h2.find_next("strong")
        if next_strong and "Unser Tipp:" in next_strong.get_text():
            tipp_text = next_strong.get_text(strip=True).replace("Unser Tipp:", "").strip()
            tips.append({
                "match": title,
                "tip": tipp_text
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
                    datum = cells[0].get_text(strip=True)
                    anstosszeit = cells[1].get_text(strip=True)
                    heimteam = cells[2].get_text(strip=True)
                    heimtea_short_name = cells[3].get_text(strip=True)
                    auswärtsteam = cells[4].get_text(strip=True).lstrip("- ").strip()
                    auswärtsteam_short_name = cells[5].get_text(strip=True)                                    
                    ergebnis = cells[6].get_text(strip=True)
                    tipp = cells[7].get_text(strip=True)

                    # Nur rot markierte Tipps extrahieren
                    if 'color: red' in cells[7].get('style', ''):
                        tipps.append({
                            'datum': datum,
                            'anstosszeit': anstosszeit,
                            'heimteam': heimteam,
                            'auswärtsteam': auswärtsteam,
                            'ergebnis': ergebnis,
                            'tipp': tipp
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
   

if __name__ == "__main__":

    all_tipps = []

    kicker_tipps = scrape_kicker_prognose()
    bundesliga_tipps = scrape_bundesliga_prognose()    
    buli_tipphilfe_tipps = scrape_buli_tipphilfe_prognose()

    all_tipps.append( kicker_tipps)
    all_tipps.append( bundesliga_tipps)
    all_tipps.append( buli_tipphilfe_tipps)
    
    print("Done")

#    for tipp in scrape_buli_tipphilfe():
#        print(f"{tipp['heimteam']} vs {tipp['auswaertsteam']} -> Tipp: {tipp['tipp']}")

 
#    for tipp in bundesliga_tipps:
#                print(f"{tipp['heimteam']} vs. {tipp['auswärtsteam']} : {tipp['tipp']}")

#    for t in kicker_tipps:
#        print(f"{t['match']}: {t['tip']}")