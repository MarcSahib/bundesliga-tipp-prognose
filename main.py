from scraper.meta import get_current_season, get_current_matchday
from scraper.kicker import scrape_kicker_prognose
from scraper.bundesliga_prognose import scrape_bundesliga_prognose
from scraper.buli_tipphilfe import scrape_buli_tipphilfe_prognose
from scraper.sportwettenvergleich import scrape_sportwettenvergleich_prognose
from scraper.ninety_min import scrape_ninety_min_prognose
from utils.normalizer import create_match_objects_by_tip_list

if __name__ == "__main__":
    current_saison = get_current_season()
    current_matchday = get_current_matchday()

    tipps = {
        "kicker": scrape_kicker_prognose(),
        "bundesliga": scrape_bundesliga_prognose(),
        "buli_tipphilfe": scrape_buli_tipphilfe_prognose(),
        "sportwettenvergleich": scrape_sportwettenvergleich_prognose(),
        "ninety_min": scrape_ninety_min_prognose(current_matchday, current_saison),
    }

    match_objects = {name: create_match_objects_by_tip_list(tlist) for name, tlist in tipps.items()}

    print("done.")
