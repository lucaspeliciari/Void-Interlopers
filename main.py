from functions import *


def game():
    pygame.init()
    pygame.display.set_caption('Void Interlopers')
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 20)

    player = Player()

    game = Game()

    interlopers = []
    populate_interlopers(interlopers, game.level)
    direction_index = 1  # + goes right, - goes left

    projectiles = []
    interloper_projectiles = []

    while True:  # check order of functions (should it calculate collisions before drawing anything?)
        clock.tick(framerate)
        screen.fill(black)

        game.game_paused = input_handler(screen, player, interlopers, projectiles, game.game_paused, game, interloper_projectiles)  # simplify

        if not game.game_paused:
            direction_index = update_interlopers(interlopers, direction_index, interloper_projectiles, game)
            update_projectiles(interloper_projectiles)
            update_projectiles(projectiles)

        draw_player(screen, player)
        draw_interlopers(screen, interlopers)
        draw_projectiles(screen, projectiles)
        draw_projectiles(screen, interloper_projectiles)
        if len(interlopers) > 0:
            draw_hud(screen, font, player, game.game_paused, False, game)
        else:
            game.game_paused = True
            draw_hud(screen, font, player, game.game_paused, True, game)

        pygame.display.flip()

        game.game_paused = collision_check(player, interlopers, projectiles, game.game_paused, game, interloper_projectiles)  # ugly but it works

        # DEBUG
        # print_mouse_coords()


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

if __name__ == '__main__':
    game()
