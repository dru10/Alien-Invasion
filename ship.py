import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    #class for managing ship behaviour
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #load ship image and get its rect
        self.image = pygame.image.load('images/ship2.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #store a decimal value for the ship's center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        #movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        #update position based on movement flags
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
            
        #update rect object from self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        
    def blitme(self):
        #draw the ship at current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #center the ship on the screen
        self.centerx = self.screen_rect.centerx
        self.centery = float(self.screen_rect.bottom) + (float(self.rect.top) - float(self.rect.bottom)) / 2
