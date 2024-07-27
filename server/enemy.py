import os, random
from typing import Any, Sequence

import pygame as pg
from server.engine import AnySprite

graveyard = os.path.join('assets', 'enemy', 'graveyard.png')

class Enemy(AnySprite):
    type = "enemy"
    max_health: int
    initial_health: list[int]
    speed: int
    hitbox: tuple[int]

    waypoints: list[Sequence[int] | pg.Vector2]
    target_waypoint: int

    pos: pg.Vector2
    movement: pg.Vector2
    health: int

    target: pg.Vector2 | tuple[int]
    movement: pg.Vector2 | tuple[int]
    def angle_right(self): return self.movement.x >= 0

    dead: bool
    death_reason: str
    
    def on_spawn(self): self.new_delta('spawn')

    def on_dead(self, reason):
        self.kill()
        self.dead = True
        self.new_delta('death')
        self.death_reason = reason
        
        if reason == 'killed':
            self.engine.enemy_downed.add(self)
        
        elif reason == 'arrived':
            self.engine.lives -= 1
            del self
    
    def on_tick_dead(self):
        if self.get_delta('death') > 150:
            self.kill()
            del self

    def on_tick(self):
        self.move()
        if self.health <= 0: self.on_dead('killed')
        if self.target_waypoint == len(self.waypoints): self.on_dead('arrived')
    
    def __init__(self, engine, waypoints):
        super().__init__(engine)
        self.engine = engine
        
        self.movement = pg.Vector2()
        self.waypoints = waypoints
        self.pos = pg.Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.target = pg.Vector2()
        
        x = self.pos.x-self.hitbox[0]//2
        y = self.pos.y-self.hitbox[1]
        self.rect = pg.Rect(x, y, self.hitbox[0], self.hitbox[1])

        self.health = random.choice(self.initial_health)
        self.dead = False

        self.on_spawn()
    
    def update(self, *args, **kwargs) -> None:
        if self.dead: self.on_tick_dead()
        else: self.on_tick()
        
        x = self.pos.x-self.hitbox[0]//2
        y = self.pos.y-self.hitbox[1]
        self.rect = pg.Rect(x, y, self.hitbox[0], self.hitbox[1])
    
    def move(self):
        """
        Move forward 
        """
        self.target = self.waypoints[self.target_waypoint]
        
        self.movement = self.target - self.pos
        distance = self.movement.length()
        self.movement = self.movement.normalize()

        if distance <= self.speed:
            self.pos = pg.Vector2(self.waypoints[self.target_waypoint])
            self.target_waypoint += 1
        else:
            self.pos += self.movement * self.speed

    def draw_properties(self) -> dict:
        return {
            'type': self.type,
            'name': self.name,
            'pos': tuple(self.pos),
            'movement': tuple(self.movement),
            'delta': self.get_all_delta()
        }

