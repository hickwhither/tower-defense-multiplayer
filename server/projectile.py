import random
from typing import Any, Sequence

import pygame as pg
from server.engine import AnySprite


class Bullet(AnySprite):
    type = 'projectile'
    name: str
    image: str
    initial_penetration: int
    drag_air: int
    drag_touch: int
    damage: int # per tick when touching
    speed: int
    hitbox: tuple[int]

    pos: pg.Vector2
    movement: pg.Vector2
    penetration: int

    def on_spawn(self): pass
    
    def on_collide_enemy(self, enemy):
        self.penetration -= self.drag_touch
        enemy.health -= self.damage

    def on_tick(self):
        self.move()
        
        for i in self.engine.enemy_group:
            if pg.sprite.collide_rect(self, i):
                self.on_collide_enemy(i)
        
        if self.penetration <= 0:
            self.kill()
            del self

    def __init__(self, engine, pos, movement):
        super().__init__(engine)
        self.engine = engine
        
        self.pos = pg.Vector2(pos)
        self.movement = pg.Vector2(movement).normalize()
        
        x = self.pos.x-self.hitbox[0]//2
        y = self.pos.y-self.hitbox[1]//2
        self.rect = pg.Rect(x, y, self.hitbox[0], self.hitbox[1])

        self.penetration = self.initial_penetration

        self.on_spawn()
    
    def update(self):
        self.on_tick()
        x = self.pos.x-self.hitbox[0]//2
        y = self.pos.y-self.hitbox[1]//2
        self.rect = pg.Rect(x, y, self.hitbox[0], self.hitbox[1])

    def move(self):
        self.pos += self.movement * self.speed
        self.penetration -= self.drag_air
    
    def draw_properties(self) -> dict:
        """
        rect:
        x,y
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, width, height
        w,h
        """
        
        return {
            'type': self.type,
            'name': self.name,
            'pos': tuple(self.pos),
            'movement': tuple(self.movement),
            'delta': self.get_all_delta()
        }

