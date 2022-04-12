from vars import *
from classes import *
import pygame
from random import randint


# POPULATE
def populate_interlopers(interlopers, level):
    formation_width = interloper_columns * interloper_width + (interloper_columns - 1) * interloper_column_step
    # formation_height = interloper_rows * interloper_height + (interloper_rows - 1) * interloper_row_step

    formation_x = (screen_width - formation_width) / 2
    formation_y = hud_area_height + 30

    # using 2d list, doesn't work yet
    # temp = []
    # for i in range(interloper_rows):
    #     for j in range(interloper_columns):
    #         temp.append(Interloper(formation_x, formation_y))
    #         formation_x += interloper_width + interloper_column_step
    #     interlopers.append(temp)
    #     formation_x = (screen_width - formation_width) / 2
    #     formation_y += interloper_height + interloper_row_step

    # using 1d list, works
    for i in range(interloper_rows):
        for j in range(interloper_columns):
            interloper = Interloper(formation_x, formation_y)
            interloper.health = level
            interlopers.append(interloper)
            formation_x += interloper_width + interloper_column_step
        formation_x = (screen_width - formation_width) / 2
        formation_y += interloper_height + interloper_row_step


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# DRAW
def draw_hud(screen, font, player, game_paused, game_won, game):
    text = font.render('VOID INTERLOPERS', 1, white)
    screen.blit(text, (screen_width / 2 - 105, 0))

    text = font.render(f'{player.score} points', 1, white)
    screen.blit(text, (4, 0))

    text = font.render(f'Level: {game.level}', 1, white)
    screen.blit(text, (0, screen_height - 21))

    text = font.render(f'Projectiles (z): {player.projectiles_fired}', 1, white)
    screen.blit(text, (0, screen_height - 84))

    text = font.render(f'Laser (x): {player.secondary_weapon_uses}', 1, white)
    screen.blit(text, (0, screen_height - 63))

    text = font.render(f'Kills: {player.kill_count}', 1, white)
    screen.blit(text, (0, screen_height - 42))

    start = screen_width - player_width - 10
    if player.lives < 6:
        for life in range(player.lives):
            pygame.draw.rect(screen, white, (start, 9, 12, 12))  # body
            pygame.draw.rect(screen, white, (start + 3, 9 - 6, 6, 6))  # cannon
            start -= player_width + 10
    else:
        pygame.draw.rect(screen, white, (start - 20, 9, 12, 12))  # body
        pygame.draw.rect(screen, white, (start - 20 + 3, 9 - 6, 6, 6))  # cannon
        text = font.render(f'x{player.lives}', 1, white)
        screen.blit(text, (start - 2, 1))

    pygame.draw.line(screen, white, (0, hud_area_height), (screen_width, hud_area_height))

    if game_paused:
        text = font.render(f'Press FIRE to start new game', 1, white)
        screen.blit(text, (screen_width - 340, screen_height - 21))

    if game_won:
        big_font = pygame.font.SysFont("monospace", 70)
        text = big_font.render(f'VICTORY!', True, white)
        screen.blit(text, (screen_width / 2 - 180, screen_height / 2 - 20))
        text = font.render(f'Now on to the next level!', 1, white)
        screen.blit(text, (screen_width / 2 - 163, screen_height / 2 + 50))

    # pygame.draw.line(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_height))


def draw_player(screen, player):
    pygame.draw.rect(screen, white, (player.x, player.y, player_width, player_height))  # body
    pygame.draw.rect(screen, white, (player.x + 3, player.y - 6, player_width / 2, player_height / 2))  # cannon


def draw_interlopers(screen, interlopers):
    for interloper in interlopers:
        interloper_color = purple
        if interloper.health == 1:
            interloper_color = red
        elif interloper.health == 2:
            interloper_color = yellow
        elif interloper.health == 3:
            interloper_color = green
        pygame.draw.rect(screen, interloper_color,
                         (interloper.x, interloper.y, interloper_width, interloper_height))  # body
        pygame.draw.circle(screen, interloper_color,
                           (interloper.x + interloper_width / 2, interloper.y + interloper_height),
                           interloper_width / 2)


def draw_projectiles(screen, projectiles):
    for projectile in projectiles:
        pygame.draw.rect(screen, red, (projectile.x, projectile.y - 10, projectile_width, projectile_height))


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# ACTIONS
def player_move(player, direction_index):
    if direction_index > 0:
        if player.x + player_width + player.speed < screen_width:
            player.x += player.speed
        else:
            player.x = screen_width - player_width
    elif direction_index < 0:
        if player.x - player.speed > 0:
            player.x -= player.speed
        else:
            player.x = 0


def player_fire(weapon_index, screen, player, interlopers, projectiles, game):
    if weapon_index == 0:
        # REGULAR PROJECTILE
        if len(projectiles) < max_projectiles_on_screen + game.level:
            projectiles.append(Projectile(player.x + 3, player.y - 6))
            player.projectiles_fired += 1
    else:
        # LASER
        if player.secondary_weapon == 'Laser' and player.secondary_weapon_uses > 0:
            player.secondary_weapon_uses -= 1
            pygame.draw.line(screen, red, (player.x + 3, player.y - 6), (player.x + 3, 0), laser_width)  # not centered
            to_remove = []
            for i, interloper in enumerate(interlopers):
                # not 100% correct
                if interloper.x + interloper_width > player.x + 3 - laser_width / 2 and interloper.x < player.x + 3 + laser_width / 2:
                    to_remove.append(i)
            destroy_objects(player, interlopers, to_remove)

        # HORIZONTAL LASER, maybe implement later
        # if player.secondary_weapon == 'Horizontal Laser' and player.secondary_weapon_uses > 0:
        #     player.secondary_weapon_uses -= 1
        #     bottom_row = [x for x in interlopers if x.x < player.x + 3 < x.x + interloper_width]
        #     print(bottom_row)
        #     to_remove = []
        #     pygame.draw.line(screen, blue, (player.x + 3, player.y - 6), (player.x + 3, 0))
        #     destroy_objects(player, interlopers, to_remove)


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# POSITIONS
def update_interlopers(interlopers, direction_index, projectiles, game):  # should move discretely, not continuously
    if len(interlopers) > 0:
        interloper_quantity = interloper_columns * interloper_rows
        current_interloper_quantity = len(interlopers)
        interloper_speed_increase = (interloper_quantity - current_interloper_quantity) / 10
        for interloper in interlopers:
            interloper.x += (base_interloper_speed + interloper_speed_increase) * direction_index

        # not moving completely to the sides if speed is too high, so player can dodge them
        interlopers_x = [x.x for x in interlopers]
        min_x = min(interlopers_x)
        max_x = max(interlopers_x)
        if max_x + interloper_width > screen_width or min_x < 0:
            for interloper in interlopers:
                interloper.y += 25
            direction_index *= -1

        # WRAPAROUND, bugged, shouldn't exist
        for interloper in interlopers:
            if interloper.y > screen_height:
                interloper.y = 0

        # FIRE
        max_shots = game.level * 3
        interloper_fire_indices = []
        for i in range(max_shots):
            if len(projectiles) < max_shots:
                interloper_fire_indices.append(randint(0, len(interlopers)))
        for i in interloper_fire_indices:
            try:  # not elegant
                projectile = Projectile(interlopers[i].x, interlopers[i].y)
                projectile.owner = 'Interloper'
                projectile.speed *= -1
                projectiles.append(projectile)
            except IndexError:
                print(i)

    return direction_index


def update_projectiles(projectiles):
    to_remove = []
    for i, projectile in enumerate(projectiles):
        projectile.y -= projectile.speed
        if projectile.y <= hud_area_height or projectile.y > screen_height:
            to_remove.append(i)

    if len(to_remove) > 0:
        for i in reversed(to_remove):
            projectiles.pop(i)


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# COLLISIONS
def collision_check(player, interlopers, projectiles, game_paused, game, interloper_projectiles):
    # PLAYER, game shouldn't respawn enemies if player has more lives remaining
    asd = game_paused  # rename the asds
    reset = 0  # 0: no reset, 1: reset game on, 2: reset game over
    for interloper in interlopers:
        if interloper.y + interloper_height > player.y and interloper.y < player.y + player_height:
            if interloper.x + interloper_width > player.x and interloper.x < player.x + player_width:
                player.lives -= 1
                if player.lives > 0:
                    reset = 1
                    break
                else:
                    reset = 2
                    break

    for projectile in interloper_projectiles:
        if projectile.y + projectile_height > player.y and projectile.y < player.y + player_height:
            if projectile.x + projectile_width > player.x and projectile.x < player.x + player_width:
                player.lives -= 1
                if player.lives > 0:
                    reset = 1
                    break
                else:
                    reset = 2
                    break

    if reset == 1:
        reset_on_game_on(player, interlopers, projectiles, game, interloper_projectiles)
    elif reset == 2:
        print('GAME OVER\nStarting new game')
        reset_on_game_over(player, interlopers, projectiles, game, interloper_projectiles)
        asd = True

    # INTERLOPERS, has a lot of bugs
    # health
    to_remove = []
    for i, projectile in enumerate(projectiles):
        if projectile.owner == 'Player':
            for j, interloper in enumerate(interlopers):
                if projectile.y < interloper.y + interloper_height and projectile.y + projectile_height > interloper.y:
                    if projectile.x + projectile_width > interloper.x and projectile.x < interloper.x + interloper_width:
                        interloper.health -= projectile.damage
                        if interloper.health <= 0:
                            to_remove.append(j)
                        projectiles.pop(i)  # shouldn't pop here

    # no health
    # to_remove = []
    # for i, projectile in enumerate(projectiles):
    #     for j, interloper in enumerate(interlopers):
    #         if projectile.y < interloper.y + interloper_height and projectile.y + projectile_height > interloper.y:
    #             if projectile.x + projectile_width > interloper.x and projectile.x < interloper.x + interloper_width:
    #                 to_remove.append(j)
    #                 projectiles.pop(i)  # shouldn't pop here

    destroy_objects(player, interlopers, to_remove)

    return asd


def destroy_objects(player, interlopers, to_remove):  # rename to destroy_interlopers?
    for i in reversed(to_remove):
        player.score += interlopers[i].score
        extend_check(player)
        player.kill_count += 1 # bugged
        interlopers.pop(i)


def extend_check(player):
    if player.score == extend_score * player.extend_multiplier:
        player.lives += 1
        player.extend_multiplier += 1


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# GAME
def reset_on_game_on(player, interlopers, projectiles, game, interloper_projectiles):
    player.reset_game_on()

    interlopers.clear()  # shouldn't reset interlopers
    populate_interlopers(interlopers, game.level)  # shouldn't reset interlopers

    projectiles.clear()
    interloper_projectiles.clear()


def reset_on_game_over(player, interlopers, projectiles, game, interloper_projectiles):
    player.reset_game_over()

    interlopers.clear()
    populate_interlopers(interlopers, game.level)

    projectiles.clear()
    interloper_projectiles.clear()


def reset_on_game_won(player, interlopers, projectiles, game, interloper_projectiles):
    game.level += 1

    player.reset_game_on()

    interlopers.clear()
    populate_interlopers(interlopers, game.level)

    projectiles.clear()
    interloper_projectiles.clear()


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# HANDLERS
def input_handler(screen, player, interlopers, projectiles, game_paused, game, interloper_projectiles):
    keys = pygame.key.get_pressed()

    if not game_paused:
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_move(player, 1)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_move(player, -1)
        # if keys[pygame.K_x]:  # hold to fire
        #     player_fire(1, screen, player, interlopers, projectiles)

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        # exit() # causing errors

    asd = game_paused
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_s or event.key == pygame.K_z:
                if not game_paused:
                    player_fire(0, screen, player, interlopers, projectiles, game)
                else:
                    if len(interlopers) <= 0:
                        reset_on_game_won(player, interlopers, projectiles, game, interloper_projectiles)
                    asd = False
            if event.key == pygame.K_x:
                if not game_paused:
                    player_fire(1, screen, player, interlopers, projectiles, game)
                else:
                    if len(interlopers) <= 0:
                        reset_on_game_won(player, interlopers, projectiles, game, interloper_projectiles)
                    asd = False

        if event.type == pygame.QUIT:
            print('Quitting')
            pygame.quit()
            exit()

    # returning game_paused
    return asd


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# DEBUG
def print_mouse_coords():
    print(pygame.mouse.get_pos())
