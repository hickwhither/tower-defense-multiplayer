import os, server.engine as engine
import pygame as pg

class Gura(engine.enemy.Enemy):
    name = "Gura"
    max_health = 10
    initial_health = [5, 6, 7, 8, 9, 10]
    speed = 4
    hitbox = [32, 32]

