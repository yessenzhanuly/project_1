import pygame

#image_path = '/data/data/com.aidyn.myapp/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption("just game")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)
bg = pygame.image.load('images/background.png').convert_alpha()

#Player
walk_left = [
    pygame.image.load('images/left_1.png').convert_alpha(),
    pygame.image.load('images/left_2.png').convert_alpha(),
    pygame.image.load('images/left_3.png').convert_alpha(),
    pygame.image.load('images/left_4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/right_1.png').convert_alpha(),
    pygame.image.load('images/right_2.png').convert_alpha(),
    pygame.image.load('images/right_3.png').convert_alpha(),
    pygame.image.load('images/right_4.png').convert_alpha(),
]

player_speed = 5
player_x = 150
player_y = 250
is_jump = False
jump_count = 8

player_anim_count = 0
bg_x = 0

#Ghost
ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_list = []
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

bg_sound = pygame.mixer.Sound('sounds/bg_music_minecraft.mp3')
bg_sound.play()

label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
lose_label = label.render('You lose!', True, (0, 0, 0))
restart_label = label.render('Play again', True, (255, 255, 255))
restart_label_rect = restart_label.get_rect(topleft=(210, 200))

bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets_left = 5
bullets = []

gameplay = True
run = True
while run:
    
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
    
        if ghost_list:
            for (i, el) in enumerate(ghost_list):
               screen.blit(ghost, el)
               el.x -= 7

               if el.x < -10:
                   ghost_list.pop(i)

               if player_rect.colliderect(el):
                   gameplay = False
    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed
    
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1
    
        bg_x -= 2
        if bg_x == -618:
            bg_x = 0
        
        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                
                if el.x > 630:
                    bullets.pop(i)
                if ghost_list:
                    for (index, ghost_i) in enumerate(ghost_list):
                        if el.colliderect(ghost_i):
                            ghost_list.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((70, 130, 180))
        screen.blit(lose_label, (210, 100))
        screen.blit(restart_label, restart_label_rect)
        
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            bullets_left = 5
            ghost_list.clear()
            bullets.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(620, 250)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 20, player_y - 15)))
            bullets_left -= 1

    clock.tick(17) 

pygame.quit()