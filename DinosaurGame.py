import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import sys
import pygame
import random

def main():

    # Initialize pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)
    pygame.init()
    random.seed()
    
    # Game Variables
    floor_x_pos = 0
    cloud_list = []
    game_active = False
    crouching = False
    floor_speed = 0
    dinosaur_jump_speed = 0
    has_jumped = False
    obstical_surface_list = []
    obstical_rect_list = []
    obstical_index_list = []
    first_game = True
    first_jump = True
    screen_index = 80
    first_ground_hit = False
    shift = 38

    # Create window and fill white
    global screen
    screen = pygame.display.set_mode((1200, 300))
    pygame.display.set_caption("Nishant's Dinosaur Game")

    # Create Clock
    clock = pygame.time.Clock()

    # script_dir is the file directory of the file
    script_dir = os.path.dirname(__file__)

    # Font
    score_font = pygame.font.Font(os.path.join(script_dir, './assets/font/PressStart2P-Regular.ttf'), 12)
    game_over_font = pygame.font.Font(os.path.join(script_dir, './assets/font/PressStart2P-Regular.ttf'), 15)

    # Floor
    floor_surface = pygame.image.load(os.path.join(script_dir, './assets/images/floor.png')).convert_alpha()
    floor_surface = pygame.transform.rotozoom(floor_surface, 0, .5)

    # Cloud
    cloud_surface = pygame.image.load(os.path.join(script_dir, './assets/images/cloud.png')).convert_alpha()
    cloud_surface = pygame.transform.rotozoom(cloud_surface, 0, .8)
    CLOUD = pygame.USEREVENT
    pygame.time.set_timer(CLOUD, 500)

    # Dinosaur
    walk_1 = pygame.image.load(os.path.join(script_dir, './assets/images/walk1.png')).convert_alpha()
    walk_1 = pygame.transform.rotozoom(walk_1, 0, .8)
    walk_2 = pygame.image.load(os.path.join(script_dir, './assets/images/walk2.png')).convert_alpha()
    walk_2 = pygame.transform.rotozoom(walk_2, 0, .8)
    duck_1 = pygame.image.load(os.path.join(script_dir, './assets/images/duck1.png')).convert_alpha()
    duck_1 = pygame.transform.rotozoom(duck_1, 0, .8)
    duck_2 = pygame.image.load(os.path.join(script_dir, './assets/images/duck2.png')).convert_alpha()
    duck_2 = pygame.transform.rotozoom(duck_2, 0, .8)
    death_image = pygame.image.load(os.path.join(script_dir, './assets/images/death2.png')).convert_alpha()
    death_image = pygame.transform.rotozoom(death_image, 0, .8)
    stand_image = pygame.image.load(os.path.join(script_dir, './assets/images/stand.png')).convert_alpha()
    stand_image = pygame.transform.rotozoom(stand_image, 0, .8)
    dinosaur_list = [walk_1, walk_2, duck_1, duck_2]
    walk_index = 0
    dinosaur_surface = dinosaur_list[walk_index]
    dinosaur_rect = dinosaur_surface.get_rect(midbottom = (80, 285))
    WALK = pygame.USEREVENT + 1
    pygame.time.set_timer(WALK, 100)

    # Cactus
    small_cactus_1 = pygame.image.load(os.path.join(script_dir, './assets/images/small_cactus1.png')).convert_alpha()
    small_cactus_1 = pygame.transform.rotozoom(small_cactus_1, 0, .8)
    small_cactus_2 = pygame.image.load(os.path.join(script_dir, './assets/images/small_cactus2.png')).convert_alpha()
    small_cactus_2 = pygame.transform.rotozoom(small_cactus_2, 0, .8)
    small_cactus_3 = pygame.image.load(os.path.join(script_dir, './assets/images/small_cactus3.png')).convert_alpha()
    small_cactus_3 = pygame.transform.rotozoom(small_cactus_3, 0, .8)
    large_cactus_1 = pygame.image.load(os.path.join(script_dir, './assets/images/large_cactus1.png')).convert_alpha()
    large_cactus_1 = pygame.transform.rotozoom(large_cactus_1, 0, .8)
    large_cactus_2 = pygame.image.load(os.path.join(script_dir, './assets/images/large_cactus2.png')).convert_alpha()
    large_cactus_2 = pygame.transform.rotozoom(large_cactus_2, 0, .8)
    large_cactus_3 = pygame.image.load(os.path.join(script_dir, './assets/images/large_cactus3.png')).convert_alpha()
    large_cactus_3 = pygame.transform.rotozoom(large_cactus_3, 0, .8)
    bird_1 = pygame.image.load(os.path.join(script_dir, './assets/images/bird1.png')).convert_alpha()
    bird_1 = pygame.transform.rotozoom(bird_1, 0, .8)
    bird_2 = pygame.image.load(os.path.join(script_dir, './assets/images/bird2.png')).convert_alpha()
    bird_2 = pygame.transform.rotozoom(bird_2, 0, .8)
    obstical_type_list = [small_cactus_1, small_cactus_2, small_cactus_3, large_cactus_1, large_cactus_2, large_cactus_3, bird_1, bird_2]
    CACTUSSPAWN = pygame.USEREVENT + 2
    pygame.time.set_timer(CACTUSSPAWN, 1000)

    # Game Over button
    game_over_button = pygame.image.load(os.path.join(script_dir, './assets/images/restart.png')).convert_alpha()
    game_over_button = pygame.transform.rotozoom(game_over_button, 0, .8)

    # Sounds
    jump_sound = pygame.mixer.Sound(os.path.join(script_dir, './assets/sounds/jump.wav'))
    death_sound = pygame.mixer.Sound(os.path.join(script_dir, './assets/sounds/death.wav'))
    point_sound = pygame.mixer.Sound(os.path.join(script_dir, './assets/sounds/point.wav'))

    # Score
    score = 0
    high_score = 0
    SCOREEVENT = pygame.USEREVENT + 10
    pygame.time.set_timer(SCOREEVENT, 100)
    
    while True:

        # Event loop
        for event in pygame.event.get():

            # Quit if window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                # Check if crouch
                if (event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT or event.key == pygame.K_s) and game_active:
                    crouching = True

                # Check if jump
                elif (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and game_active:
                    if not(has_jumped):
                        dinosaur_jump_speed = 10
                        jump_sound.play()

                # Reset Game
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and not(game_active) and not(first_game):
                    dinosaur_rect = dinosaur_surface.get_rect(midbottom = (80, 285))
                    if score > high_score:
                        high_score = score
                    obstical_index_list.clear()
                    obstical_rect_list.clear()
                    obstical_surface_list.clear()
                    floor_speed = 4
                    dinosaur_jump_speed = 0
                    score = 0
                    crouching = False
                    jump_sound.play()
                    game_active = True
                elif (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and not(game_active) and first_game:
                    dinosaur_jump_speed = 10
                    jump_sound.play()
                    
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_LSHIFT or event.key == pygame.K_s) and game_active:
                    crouching = False

            # Spawn Cloud
            if event.type == CLOUD and game_active:
                if random.randint(1, 10) == 1:
                    cloud_list.append(create_cloud(cloud_surface))

            # Walk animation
            if event.type == WALK and not(crouching) and game_active:
                if walk_index != 0:
                    walk_index = 0
                else:
                    walk_index = 1
                dinosaur_surface, dinosaur_rect = dino_animation(walk_index, dinosaur_list, dinosaur_rect)
            elif event.type == WALK and crouching and game_active:
                if walk_index != 2:
                    walk_index = 2
                else:
                    walk_index = 3
                dinosaur_surface, dinosaur_rect = dino_animation(walk_index, dinosaur_list, dinosaur_rect)
            
            # Spawn Cactus
            if event.type == CACTUSSPAWN and game_active:
                if random.randint(1,100) > 10 - score // 300:
                    temp_surface, temp_rect, temp_index = spawn_cactus(obstical_type_list, score)
                    obstical_surface_list.append(temp_surface)
                    obstical_rect_list.append(temp_rect)
                    obstical_index_list.append(temp_index)

                # Remove Cactus
                obstical_surface_list, obstical_rect_list, obstical_index_list = remove_cactus(obstical_surface_list, obstical_rect_list, obstical_index_list)

            # Score
            if event.type == SCOREEVENT and game_active:
                score += 1
                if score % 100 == 0:
                    point_sound.play()
                    floor_speed += 1
                if score % 150 == 0 and score < 900:
                    pygame.time.set_timer(CACTUSSPAWN, 1000 - score // 3)

        screen.fill((255, 255, 255))

        # Clouds
        if game_active:
            cloud_list = move_clouds(cloud_list)
        draw_clouds(cloud_list, cloud_surface, screen)

        # Floor
        floor_x_pos -= floor_speed
        draw_floor(floor_x_pos, floor_surface)
        if floor_x_pos <= -1200:
            floor_x_pos = 0

        # Cactus
        obstical_rect_list = move_cactus(obstical_rect_list, floor_speed)
        draw_cactus(obstical_surface_list, obstical_rect_list, obstical_index_list)
        if game_active:
            obstical_surface_list, obstical_index_list = animate_bird(obstical_index_list, obstical_surface_list, obstical_type_list)
        
        # Dinosaur
        dinosaur_rect.bottom -= dinosaur_jump_speed
        if dino_on_ground(dinosaur_rect):
            has_jumped = False
            dinosaur_rect.bottom = 285
            dinosaur_jump_speed = 0
        else:
            has_jumped = True
            if game_active or first_game:
                dinosaur_jump_speed -= 0.3
                if first_game and dinosaur_rect.bottom < 210:
                    first_jump = False
            else:
                dinosaur_jump_speed = 0
        if game_active == False:
            dinosaur_surface = death_image
            dinosaur_rect = dinosaur_surface.get_rect(midbottom = (83, dinosaur_rect.bottom))
        if not(first_game):
            screen.blit(dinosaur_surface, dinosaur_rect)

        # Collision detection and changes
        if check_collision(dinosaur_rect, obstical_rect_list):
            floor_speed = 0
            if game_active:
                death_sound.play()
            game_active = False
            
        if game_active == False:
             game_over_display(screen, game_over_font, game_over_button, first_game)   

        # Score
        display_score(score, high_score, score_font, screen)

        # First Game
        if first_game and not(game_active):
            if first_ground_hit == False:
                dinosaur_surface = stand_image
                dinosaur_rect = dinosaur_surface.get_rect(midbottom = (38, dinosaur_rect.bottom))
                screen.blit(dinosaur_surface, dinosaur_rect)
            if first_jump:
                pygame.draw.rect(screen, (255, 255, 255), (screen_index, 0, 1220, 300))
            else:
                screen_index += 5
                pygame.draw.rect(screen, (255, 255, 255), (screen_index, 0, 1220, 300))
                if dino_on_ground(dinosaur_rect) or first_ground_hit:
                    first_ground_hit = True
                    floor_speed = 4
                    if walk_index != 0:
                        walk_index = 0
                    else:
                        walk_index = 1
                    dinosaur_surface = dinosaur_list[walk_index]
                    dinosaur_rect = dinosaur_surface.get_rect(midbottom = (shift, dinosaur_rect.bottom))
                    if shift < 83:
                        shift += 1
                    if screen_index == 1200:
                        first_game = False
                        game_active = True
                    screen.blit(dinosaur_surface, dinosaur_rect)
        pygame.display.update()
        clock.tick(120)

def draw_floor(floor_x_pos, floor_surface):
    screen.blit(floor_surface, (floor_x_pos, 275))
    screen.blit(floor_surface, (floor_x_pos + 1200, 275))

def create_cloud(cloud_surface):
    cloud_rect = cloud_surface.get_rect(center = (1300, random.randint(50, 125)))
    return cloud_rect

def move_clouds(clouds):
    for cloud in clouds:
        cloud.centerx -= 1

        if cloud.right <= -10:
            clouds.remove(cloud)

    return clouds

def draw_clouds(clouds, cloud_surface, screen):
    for cloud in clouds:
        screen.blit(cloud_surface, cloud)

def display_score(score, high_score, game_font, screen):
    if score < 100 or score % 100 > 25:
        score_surface = game_font.render('{:05d}'.format(score), True, (83, 83, 83))
    elif score % 100 <= 5:
        score_surface = game_font.render('     ', True, (83, 83, 83))
    elif score % 100 <= 10:
        score_surface = game_font.render('{:05d}'.format(score // 100 * 100), True, (83, 83, 83))
    elif score % 100 <= 15:
        score_surface = game_font.render('     ', True, (83, 83, 83))
    elif score % 100 <= 20:
        score_surface = game_font.render('{:05d}'.format(score // 100 * 100), True, (83, 83, 83))
    elif score % 100 <= 25:
        score_surface = game_font.render('     ', True, (83, 83, 83))
    
    score_rect = score_surface.get_rect(midright = (1190, 20))
    screen.blit(score_surface, score_rect)

    high_score_surface = game_font.render('HI {:05d}'.format(high_score), True, (117, 117, 117))
    high_score_rect = high_score_surface.get_rect(midright = (1120, 20))
    screen.blit(high_score_surface, high_score_rect)

def dino_animation(dino_index, dinosaur_list, dinosaur_rect):
    dino = dinosaur_list[dino_index]
    dino_rect = dino.get_rect(midbottom = (dinosaur_rect.centerx, dinosaur_rect.bottom))
    return dino, dino_rect

def dino_on_ground(dinosaur_rect):
    if dinosaur_rect.bottom >= 285:
        return True
    else:
        return False

def spawn_cactus(obstical_type_list, score):
    heights = [205, 235, 285]
    rand = 0
    if score <= 200:
        index = random.randint(0,4)
    elif 200 < score <= 400:
        index = random.randint(0,5)
        rand = random.randint(-10, 10)
    else:
        index = random.randint(0,7)
        rand = random.randint(-25, 25)
    cactus_surface = obstical_type_list[index]
    if index < 6:
        cactus_rect = cactus_surface.get_rect(midbottom = (1300 + rand, 290))
    else:
        cactus_rect = cactus_surface.get_rect(midbottom = (1300, random.choice(heights)))
    return cactus_surface, cactus_rect, index

def move_cactus(obstical_rect_list, floor_speed):
    for cactus in obstical_rect_list:
        cactus.centerx -= floor_speed
    return obstical_rect_list

def draw_cactus(obstical_surface_list, obstical_rect_list, obstical_index_list):
    for x in range(len(obstical_rect_list)):
        screen.blit(obstical_surface_list[x], obstical_rect_list[x])

def remove_cactus(obstical_surface_list, obstical_rect_list, obstical_index_list):
    
    for rect in obstical_rect_list:
        if rect.centerx <= -100:
            del obstical_surface_list[0:1]
            del obstical_rect_list[0:1]
            del obstical_index_list[0:1]
    return obstical_surface_list, obstical_rect_list, obstical_index_list

def animate_bird(obstical_index_list, obstical_surface_list, obstical_type_list):
    for x in range(len(obstical_index_list)):
        if obstical_index_list[x] == 6:
            obstical_surface_list[x] = obstical_type_list[6]
            obstical_index_list[x] = 7
        elif obstical_index_list[x] == 7:
            obstical_surface_list[x] = obstical_type_list[7]
            obstical_index_list[x] = 6
    return obstical_surface_list, obstical_index_list

def check_collision(single_rect, rect_list):
    for rect in rect_list:
        if single_rect.colliderect(rect):
            return True
    return False

def game_over_display(screen, game_over_font, game_over_button, first_game):
    if not(first_game):
        game_over_surface = game_over_font.render('G A M E   O V E R', True, (83, 83, 83))
        game_over_rect = game_over_surface.get_rect(midtop = (600, 80))
        screen.blit(game_over_surface, game_over_rect)

        button_rect = game_over_button.get_rect(center = (600, 150))
        screen.blit(game_over_button, button_rect)

if __name__ == '__main__':
    main()