import json


class GameStats():
    #track stats for Alien Invasion
    
    def __init__(self, ai_settings):
        #high score should never be reset
        filename = 'high_score.json'
        try:
            with open(filename) as file:
                self.high_score = json.load(file)
        except FileNotFoundError:
            self.high_score = 0
        
        #initialize stats
        self.ai_settings = ai_settings
        self.reset_stats()
        
        #start Alien Invasion in an inactive state
        self.game_active = False
        
    def reset_stats(self):
        #initialize statistics that change during the game
        self.ships_left = self.ai_settings.ships_limit
        self.score = 0
        self.level = 1
