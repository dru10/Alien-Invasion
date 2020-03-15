import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #class to represent single alien of fleet
    def __init__(self, ai_settings, screen):
        #initialze alien and set start position
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #load the alien image
        self.image = pygame.image.load('images/alien_ship.bmp')
        self.rect = self.image.get_rect()
        
        #start each new alien at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store alien exact position
        self.x = float(self.rect.x)
        
    def blitme(self):
        #draw the alien at current location
        self.screen.blit(self.image, self.rect)
        
    def check_edges(self):
        #return true if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        #move the alien right
        self.x += (self.ai_settings.alien_speed_factor * 
            self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
