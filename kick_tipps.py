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


   

if __name__ == "__main__":

    all_tipps = []

    kicker_tipps = scrape_kicker_prognose()
    all_tipps.append(kicker_tipps)
   
    # bundesliga_tipps = scrape_bundesliga_prognose()
    # for t in bundesliga_tipps:
    #    print(f"{t['date']} {t['time']}: {t['home_team']} vs. {t['away_team']} -> {t['tip']} (Ergebnis: {t['result']})")



#    for t in kicker_tipps:
#        print(f"{t['match']}: {t['tip']}")