import os, server.engine as engine

class rock_1(engine.projectile.Bullet):
    name = "rock_1"
    initial_penetration = 160
    drag_air = 1
    drag_touch = 320
    damage = 3
    speed = 5
    hitbox = [8, 8]

