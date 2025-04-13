class Match:
    def __init__(self, home_team, away_team, tip):
        self._home_team = home_team
        self._away_team = away_team
        self._tip = tip
    
    # Getter für das Home-Team
    def get_home_team(self):
        return self._home_team
    
    # Setter für das Home-Team
    def set_home_team(self, home_team):
        self._home_team = home_team
    
    # Getter für das Auswärts-Team
    def get_away_team(self):
        return self._away_team
    
    # Setter für das Auswärts-Team
    def set_away_team(self, away_team):
        self._away_team = away_team
    
    # Getter für den Tipp
    def get_tip(self):
        return self._tip
    
    # Setter für den Tipp
    def set_tip(self, tip):
        self._tip = tip
    
    # Methode, um das Match zu beschreiben
    def __str__(self):
        return f"{self._home_team} vs. {self._away_team} - Tipp: {self._tip}"
