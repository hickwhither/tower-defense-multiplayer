import os, server.engine as engine

def setup(game: engine.Engine) -> None:
    game.add_index(rock_1)
    game.add_index(rock_2)

class rock_1(engine.Bullet):
    name = "rock_1"
    image = os.path.join('assets', 'projectile', 'rock_1.png')
    initial_penetration = 160
    drag_air = 1
    drag_touch = 320
    damage = 3
    speed = 5
    hitbox = [8, 8]

class rock_2(engine.Bullet):
    name = "rock_2"
    image = os.path.join('assets', 'projectile', 'rock_2.png')
    initial_penetration = 320
    drag_air = 1
    drag_touch = 960
    damage = 1
    speed = 10
    hitbox = [8, 8]

