import os, server.engine as engine
import pygame as pg

class TriBede(engine.enemy.Enemy):
    name = "TriBede"
    max_health = 5
    initial_health = [1, 3, 4, 5]
    speed = 2
    hitbox = [69, 95]

