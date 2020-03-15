import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    #class that manages bullets fired from ship
    
    def __init__(self, ai_settings, screen, ship):
        #create bullet at ship's current position
        super().__init__()
        self.screen = screen
    
        #create bullet at (0,0) then set correct postion
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #store bullet position as decimal value
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        #move the bullet up the screen
        #update decimal position of bullet
        self.y -= self.speed_factor
        #update rect position
        self.rect.y = self.y
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
