import requests
from bs4 import BeautifulSoup
import re

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