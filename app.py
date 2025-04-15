from flask import Flask, render_template, request
from scraper.meta import get_current_season, get_current_matchday
from scraper.kicker import scrape_kicker_prognose
from scraper.bundesliga_prognose import scrape_bundesliga_prognose
from scraper.buli_tipphilfe import scrape_buli_tipphilfe_prognose
from scraper.sportwettenvergleich import scrape_sportwettenvergleich_prognose
from scraper.ninety_min import scrape_ninety_min_prognose
from utils.normalizer import create_match_objects_by_tip_list

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", match_objects=None)

@app.route("/scrape", methods=["POST"])
def scrape():
    saison = get_current_season()
    spieltag = get_current_matchday()

    tipps = {
        "kicker": scrape_kicker_prognose(),
        "bundesliga": scrape_bundesliga_prognose(),
        "buli_tipphilfe": scrape_buli_tipphilfe_prognose(),
        "sportwettenvergleich": scrape_sportwettenvergleich_prognose(),
        "ninety_min": scrape_ninety_min_prognose(spieltag, saison),
    }

    match_objects = {
        name: create_match_objects_by_tip_list(tlist)
        for name, tlist in tipps.items()
    }

    return render_template("index.html", match_objects=match_objects)

if __name__ == "__main__":
    app.run(debug=True)
