import os, server.engine as engine

class rock_2(engine.projectile.Bullet):
    name = "rock_2"
    initial_penetration = 320
    drag_air = 1
    drag_touch = 960
    damage = 1
    speed = 10
    hitbox = [8, 8]

