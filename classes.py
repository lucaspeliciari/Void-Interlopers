from vars import screen_width, screen_height, projectile_speed, player_speed


class Player():
    def __init__(self):
        self.score = 0
        self.x = screen_width / 2
        self.y = screen_height - 20
        self.speed = player_speed
        self.lives = 3
        self.extend_multiplier = 1
        self.kill_count = 0
        self.secondary_weapon = 'Laser'
        self.secondary_weapon_uses = 5
        self.projectiles_fired = 0

    def reset_game_on(self):
        self.x = screen_width / 2
        self.y = screen_height - 20
        self.speed = player_speed

    def reset_game_over(self):
        self.score = 0
        self.x = screen_width / 2
        self.y = screen_height - 20
        self.speed = player_speed
        self.lives = 3
        self.extend_multiplier = 1
        self.secondary_weapon = 'Laser'
        self.secondary_weapon_uses = 5


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class Projectile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = projectile_speed
        self.owner = 'Player'
        self.damage = 1


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class Interloper():
    def __init__(self, x, y):
        self.score = 100
        self.x = x
        self.y = y
        self.health = 2

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


class Game():  # put all lists in here
    def __init__(self):
        self.game_paused = True
        self.level = 1
        # self.player # use all this
        self.interlopers = []
        self.projectiles = []
        self.interloper_projectiles = []
