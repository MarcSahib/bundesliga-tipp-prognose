from model.match import Match
from utils.constants import BUNDESLIGA_TEAMS, BUNDESLIGA_TEAM_CITIES

def normalize_team_name(team_name):
    team_name_lower = team_name.lower()
    for i, city_aliases in enumerate(BUNDESLIGA_TEAM_CITIES):
        if any(alias in team_name_lower for alias in city_aliases):
            return BUNDESLIGA_TEAMS[i]
    return team_name  # Falls kein Match

def create_match_objects_by_tip_list(tip_list):
    
    match_objects = []

    for tip in tip_list:

        tip["home_team"] = normalize_team_name(tip["home_team"])
        tip["away_team"] = normalize_team_name(tip["away_team"])

        if tip["home_team"] not in BUNDESLIGA_TEAMS:
            print(f'Home Team not found: {tip["home_team"]}') 
        if tip["away_team"] not in BUNDESLIGA_TEAMS:
            print(f'Away Team not found: {tip["away_team"]}')

        match = Match(
            tip["home_team"], 
            tip["away_team"], 
            tip["home_goals_tip"],
            tip["away_goals_tip"],
            tip["tip"], 
            tip["date"], 
            tip["kickoff_time"], 
            tip["result"] )
        
        match_objects.append(match)

    return match_objects