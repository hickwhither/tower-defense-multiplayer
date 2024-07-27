import random
from typing import Any, Sequence

import pygame as pg
from projectile import *

towerplot_img = None

class TowerPlot:
    type = "towerplot"
    name: str
    pos: pg.Vector2

    start_time: int
    tower: 'Tower'
    
    def __init__(self, pos):
        self.pos = pos
        self.tower = None
    
    def tower_place(self, tower):
        self.tower=tower
        self.start_time = pg.time.get_ticks()
    
    def tower_destroy(self):
        self.tower = None
        self.start_time = pg.time.get_ticks()
    
    def update(self):
        if self.tower==None: return
        self.tower.update()


    def draw_properties(self) -> dict:
        draw = {
                'image': towerplot_img,
                'rect': {'center': self.pos}
            }
        if self.tower:
            draw['image'] = self.tower.get_image()
            pos = self.pos.copy()
            pos.x -= self.tower.height_center
            draw['rect'] = {'midbottom': pos}
        
        return draw
class TowerStage:
    projectiles: list
    projectiles_delay: list[int]

class Tower:
    type = "tower"
    name: str
    height_center: int

    towerstages: list[TowerStage]
    
    projectiles: list
    projectiles_delay: list[int]
    projectiles_group = pg.sprite.Group

    def __init__(self):
        ...
    
    def update(self): ...

    def get_image(self): ...
    
    