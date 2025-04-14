from model.match import Match
from utils.constants import BUNDESLIGA_TEAMS

def create_match_objects_by_tip_list(tip_list):
    
    match_objects = []

    for tip in tip_list:

        if "Augsburg".lower() in tip["home_team"].lower():
            tip["home_team"] = "FC Augsburg"
        if "Augsburg".lower() in tip["away_team"].lower():
            tip["away_team"] = "FC Augsburg"

        if "Bayern".lower() in tip["home_team"].lower():
            tip["home_team"] = "FC Bayern München"
        if "Bayern".lower() in tip["away_team"].lower():
            tip["away_team"] = "FC Bayern München"

        if "Bochum".lower() in tip["home_team"].lower():
            tip["home_team"] = "VfL Bochum"
        if "Bochum".lower() in tip["away_team"].lower():
            tip["away_team"] = "VfL Bochum"

        if "Bremen".lower() in tip["home_team"].lower():
            tip["home_team"] = "SV Werder Bremen"
        if "Bremen".lower() in tip["away_team"].lower():
            tip["away_team"] = "SV Werder Bremen"

        if "Dortmund".lower() in tip["home_team"].lower() or "BVB" in tip["home_team"]:
            tip["home_team"] = "Borussia Dortmund"
        if "Dortmund".lower() in tip["away_team"].lower() or "BVB" in tip["away_team"]:
            tip["away_team"] = "Borussia Dortmund"

        if "Frankfurt".lower() in tip["home_team"].lower():
            tip["home_team"] = "Eintracht Frankfurt"
        if "Frankfurt".lower() in tip["away_team"].lower():
            tip["away_team"] = "Eintracht Frankfurt"

        if "Freiburg".lower() in tip["home_team"].lower():
            tip["home_team"] = "SC Freiburg"
        if "Freiburg".lower() in tip["away_team"].lower():
            tip["away_team"] = "SC Freiburg"

        if "Gladbach".lower() in tip["home_team"].lower():
            tip["home_team"] = "Bor. Mönchengladbach"
        if "Gladbach".lower() in tip["away_team"].lower():
            tip["away_team"] = "Bor. Mönchengladbach"
        
        if "Heidenheim".lower() in tip["home_team"].lower():
            tip["home_team"] = "1.FC Heidenheim"
        if "Heidenheim".lower() in tip["away_team"].lower():
            tip["away_team"] = "1.FC Heidenheim"

        if "Hoffenheim".lower() in tip["home_team"].lower():
            tip["home_team"] = "TSG Hoffenheim"
        if "Hoffenheim".lower() in tip["away_team"].lower():
            tip["away_team"] = "TSG Hoffenheim"

        if "Kiel".lower() in tip["home_team"].lower():
            tip["home_team"] = "Holstein Kiel"
        if "Kiel".lower() in tip["away_team"].lower():
            tip["away_team"] = "Holstein Kiel"
        
        if "Leipzig".lower() in tip["home_team"].lower():
            tip["home_team"] = "RB Leipzig"
        if "Leipzig".lower() in tip["away_team"].lower():
            tip["away_team"] = "RB Leipzig"

        if "Leverkusen".lower() in tip["home_team"].lower():
            tip["home_team"] = "Bayer 04 Leverkusen"
        if "Leverkusen".lower() in tip["away_team"].lower():
            tip["away_team"] = "Bayer 04 Leverkusen"

        if "Mainz".lower() in tip["home_team"].lower():
            tip["home_team"] = "1.FSV Mainz 05"
        if "Mainz".lower() in tip["away_team"].lower():
            tip["away_team"] = "1.FSV Mainz 05"

        if "Pauli".lower() in tip["home_team"].lower():
            tip["home_team"] = "FC St. Pauli"
        if "Pauli".lower() in tip["away_team"].lower():
            tip["away_team"] = "FC St. Pauli"

        if "Stuttgart".lower() in tip["home_team"].lower():
            tip["home_team"] = "VfB Stuttgart"
        if "Stuttgart".lower() in tip["away_team"].lower():
            tip["away_team"] = "VfB Stuttgart"
        
        if "Union".lower() in tip["home_team"].lower():
            tip["home_team"] = "1.FC Union Berlin"
        if "Union".lower() in tip["away_team"].lower():
            tip["away_team"] = "1.FC Union Berlin"

        if "Wolfsburg".lower() in tip["home_team"].lower():
            tip["home_team"] = "VfL Wolfsburg"
        if "Wolfsburg".lower() in tip["away_team"].lower():
            tip["away_team"] = "VfL Wolfsburg"
    
        if tip["home_team"] not in BUNDESLIGA_TEAMS:
            print(f'Home Team not found: {tip["home_team"]}')
        if tip["away_team"] not in BUNDESLIGA_TEAMS:
            print(f'Away Team not found: {tip["away_team"]}')

        match = Match(
            tip["home_team"], 
            tip["away_team"], 
            tip["tip"], 
            tip["date"], 
            tip["kickoff_time"], 
            tip["result"] )
        
        match_objects.append(match)

    return match_objects