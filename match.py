class Match: # match = Match(tip["home_team"], tip["away_team"], tip["date"], tip["kickoff_time"], tip["result"] )
    def __init__(self, home_team, away_team, tip, date=None, kickoff_time=None, result=None):

        self._home_team = home_team
        self._away_team = away_team
        self._tip = tip
        self._date = date
        self._kickoff_time = kickoff_time
        self._result = result
        

    def get_date(self):
        return self._date
    
    def set_date(self, date):
        self._date = date

    def get_kickoff_time(self):
        return self._kickoff_time
    
    def set_kickoff_time(self, kickoff_time):
        self._kickoff_time = kickoff_time

    def get_home_team(self):
        return self._home_team
    
    def set_home_team(self, home_team):
        self._home_team = home_team
    
    def get_away_team(self):
        return self._away_team
    
    def set_away_team(self, away_team):
        self._away_team = away_team
    
    def get_tip(self):
        return self._tip
    
    def set_tip(self, tip):
        self._tip = tip

    def get_result(self):
        return self._result
    
    def set_result(self, result):
        self._result = result
    
    def __str__(self):
        return f"{self._home_team} vs. {self._away_team} - Tipp: {self._tip}"
