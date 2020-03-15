import sys
from time import sleep
import pygame
import json

from bullet import Bullet
from alien import Alien


def check_high_score(stats, sb):
    #check to see if there is new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def fire_bullet(ai_settings, screen, ship, bullets):
    #fire bullet if limit not reached
    #create new bullet and add it to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def save_high_score(stats):
    filename = 'high_score.json'
    with open(filename, 'w') as file:
        json.dump(stats.high_score, file)
        
def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    #respond to keypresses
    if event.key == pygame.K_RIGHT:
        #move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        save_high_score(stats)
        sys.exit()

def check_keyup_events(event, ship):
    #respond to key releases
    if event.key == pygame.K_RIGHT:
        #stop moving the ship to the right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
    bullets):
    #respond to keypresses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit(stats)
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, 
                ship, bullets)
                    
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb,  play_button,
                ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
    aliens, bullets, mouse_x, mouse_y):
    #start new game when player clicks play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset game settings
        ai_settings.initialize_dynamic_settings()
        
        #hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        #reset stats
        stats.reset_stats()
        stats.game_active = True
        
        #reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #create fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
    play_button):
    #update images on the screen
    #redraw the screen during each pass through the loop       
    screen.fill(ai_settings.bg_color)
    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    #draw score information
    sb.show_score()
    
    #draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
        
    #make the most recent screen visible
    pygame.display.flip()
        
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #update position of bullets and get rid of old bullets
    #update bullet positions
    bullets.update()
        
    #delete bullets that disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
        aliens, bullets)
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
    aliens, bullets):
    #check for any bullets that have hit aliens
    # if so, get rid of bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        
    if len(aliens) == 0:
        #if entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()
        
        #increase level
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
            
def get_number_aliens_x(ai_settings, alien_width):
    #determine number of aliens that fit in a row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    #determine the number of rows of aliens that fit on the screen
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - 
        ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    #create a full fleet of aliens
    #create alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
        alien.rect.height)
    
    #create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, 
                row_number)
                
def check_fleet_edges(ai_settings, aliens):
    #respond appropriately if any aliens reach the edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
            
def change_fleet_direction(ai_settings, aliens):
    #drop entire fleet and change its direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #respond to ship being hit by alien
    if stats.ships_left > 0: 
        stats.ships_left -= 1
        
        #update scoreboard
        sb.prep_ships()
        
        #empty list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #create new fleet and center ship
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)
        
        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #check if aliens have reached bottom of screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat as if ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
                
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #update the position of all aliens in the fleet
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
    #look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
