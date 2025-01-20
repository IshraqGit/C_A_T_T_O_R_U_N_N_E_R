import pygame
from sys import exit
from random import randint

#Calculates the score and displays it on the right hand side of the sccreen (blits it)
def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, 'White')
    score_rect = score_surf.get_rect(center=(700, 50))
    screen.blit(score_surf, score_rect)
    return current_time

#creats the number of enemies to be spawn in the gameplay screen
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

            if obstacle_rect.bottom == 300:
                screen.blit(egg_surf, obstacle_rect)
            else:
                screen.blit(sushi_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

#detects collision btwn player and enemy
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

#player jump+ player walk
def player_animation():
    global player_surf, player_index, player_rect

    if player_rect.bottom < 300:
        player_surf = player_jump
        
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


def main():
    global screen, test_font, clock
    global sky_surface, ground_surface, egg_surf, sushi_surf
    global player_surf, player_rect, player_gravity, player_index
    global player_walk, player_jump, obstacle_rect_list
    global game_active, start_time, score
    global player_stand_screen, player_stand_rect, player_stand_index
    global egg_frames, egg_frame_index, sushi_frames, sushi_frame_index

    #general configuration of the gamee
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('CattoRunner')
    clock = pygame.time.Clock()
    test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    game_active = False
    start_time = 0
    score = 0

    #Background image load from the directory
    sky_surface = pygame.image.load('graphics/bg.png').convert()
    ground_surface = pygame.image.load('graphics/bricking.png').convert()

    #Background Music ( main menu and gameplay )
    bg_music = pygame.mixer.Sound('audio/game_on.mp3')  
    bg_music.set_volume(0.8)

    main_menu_music = pygame.mixer.Sound('audio/main_menu.wav')  
    main_menu_music.set_volume(0.1)
    

    #Sound Effects (for player jump and collision)
    collision_sound = pygame.mixer.Sound('audio/collision.mp3')  
    collision_sound.set_volume(0.5)
    jump_sound = pygame.mixer.Sound('audio/jump.mp3')  
    jump_sound.set_volume(0.8)
    

    #Obstacles loaded from the directory and prepared to be passed the the function for processing
    egg_frame_1 = pygame.image.load('graphics/Egg/egg_1.png').convert_alpha()
    egg_frame_1 = pygame.transform.scale(egg_frame_1,(80,80))
    egg_frame_2 = pygame.image.load('graphics/Egg/egg_2.png').convert_alpha()
    egg_frame_2 = pygame.transform.scale(egg_frame_2,(80,80))
    egg_frames = [egg_frame_1, egg_frame_2]
    egg_frame_index = 0
    egg_surf = egg_frames[egg_frame_index]

    sushi_frame_1 = pygame.image.load('graphics/Sushi/sushi_1.png').convert_alpha()
    sushi_frame_1 = pygame.transform.scale(sushi_frame_1,(120,120))
    sushi_frame_2 = pygame.image.load('graphics/Sushi/sushi_2.png').convert_alpha()
    sushi_frame_2 = pygame.transform.scale(sushi_frame_2,(120,120))

    sushi_frames = [sushi_frame_1, sushi_frame_2]
    sushi_frame_index = 0
    sushi_surf = sushi_frames[sushi_frame_index]

    obstacle_rect_list = []

    #Player loaded and to be passed
    player_walk_1 = pygame.image.load('graphics/player/hk_1.png').convert_alpha()
    player_walk_2 = pygame.image.load('graphics/player/hk_2.png').convert_alpha()
    player_walk = [player_walk_1, player_walk_2]
    player_index = 0
    player_jump = pygame.image.load('graphics/player/hk_3.png').convert_alpha()

    player_surf = player_walk[player_index]
    player_rect = player_surf.get_rect(midbottom=(80, 300))
    player_gravity = 0

    #Intro Screen ( default start up screen that user sees)
    player_stand_1 = pygame.image.load('graphics/player/cat_2.png').convert_alpha()
    player_stand_2 = pygame.image.load('graphics/player/cat_3.png').convert_alpha()
    player_stand_1 = pygame.transform.rotozoom(player_stand_1, 0, 0.25)
    player_stand_2 = pygame.transform.rotozoom(player_stand_2, 0, 0.25)
    player_stand_frames = [player_stand_1, player_stand_2]
    player_stand_index = 0
    player_stand_screen = player_stand_frames[player_stand_index]
    player_stand_rect = player_stand_screen.get_rect(center=(400, 200))

    game_name = test_font.render("C A T T O R U N N E R", False, (240, 112, 70))
    game_name = pygame.transform.rotozoom(game_name, 0, 2)
    game_name_rect = game_name.get_rect(center=(400, 70))

    bot_text = test_font.render('PRESS SPACE TO RUN', False, 'Black')
    bot_text_rect = bot_text.get_rect(center=(400, 370))

    #Timers for player total obstacle and egg+sushi along with load screen
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1200)

    egg_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(egg_animation_timer, 500)

    sushi_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(sushi_animation_timer, 200)

    load_screen_timer = pygame.USEREVENT + 4
    pygame.time.set_timer(load_screen_timer, 1000)

    while True:
        #events in the game
        for event in pygame.event.get():
            #game quiting
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # user instructions keyboard,mouse
            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                        player_gravity = -20 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                        player_gravity = -20
                        #jump sound
                        jump_sound.play()
                #spawing the obstacles in the main game
                if event.type == obstacle_timer:
                    if randint(0, 2):
                        obstacle_rect_list.append(egg_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                    else:
                        obstacle_rect_list.append(sushi_surf.get_rect(bottomright=(randint(900, 1100), 200)))

                if event.type == egg_animation_timer:
                    egg_frame_index = (egg_frame_index + 1) % len(egg_frames)
                    egg_surf = egg_frames[egg_frame_index]

                if event.type == sushi_animation_timer:
                    sushi_frame_index = (sushi_frame_index + 1) % len(sushi_frames)
                    sushi_surf = sushi_frames[sushi_frame_index]

            else:
                #when game stops
                if event.type == load_screen_timer:
                    player_stand_index = (player_stand_index + 1) % len(player_stand_frames)
                    player_stand_screen = player_stand_frames[player_stand_index]

                #restart the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    #music
                    main_menu_music.stop()
                    bg_music.play(-1)  #Loop indefinitely
                    start_time = int(pygame.time.get_ticks() / 100)

        if game_active:
            screen.blit(sky_surface, (0,0))
            screen.blit(ground_surface, (0, 300))
            
            #Score
            score = display_score()

            #Player
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300
            player_animation()
            screen.blit(player_surf, player_rect)

            #Obstacles
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            #Collisions
            game_active = collisions(player_rect, obstacle_rect_list)
            if(not game_active):
                collision_sound.play()
            

        else:
            #music restart
            bg_music.stop()
            main_menu_music.play()

            screen.fill((94, 129, 162))
            screen.blit(player_stand_screen, player_stand_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80, 300)
            player_gravity = 0

            #initially screen does not need a score, only display it after a gaming encounter
            if score > 0:
                score_message = test_font.render(f'Your Score: {score}', False, 'White')
                score_message_rect = score_message.get_rect(center=(400, 330))
                screen.blit(score_message, score_message_rect)

            screen.blit(game_name, game_name_rect)
            screen.blit(bot_text, bot_text_rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
