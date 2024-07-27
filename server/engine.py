import constants_server as c

import json, random
import os, importlib.util
from typing import Any, Sequence

import pygame as pg

import server.errors as errors
import map.test_gura.behavior as behavior

class AnySprite(pg.sprite.Sprite):
    type: str
    name: str

    start_time: dict[int]
    engine: 'Engine'

    def __init__(self, engine: 'Engine', *args, **kwawrgs):
        super().__init__(*args, **kwawrgs)
        self.engine = engine
        self.start_time = {}
    
    def new_delta(self, name) -> None: self.start_time[name] = self.engine.tick
    def get_delta(self, name) -> int: return self.engine.tick - self.start_time[name]
    def get_all_delta(self) -> dict:
        delta_time = {}
        current_time = self.engine.tick
        for i in self.start_time:
            delta_time[i] = current_time - self.start_time[i]
        return delta_time

from . import enemy
class Engine:
    enemy_index: dict[enemy.Enemy]

    lives: int

    enemy_group: pg.sprite.Group
    tower_group: pg.sprite.Group
    projectile_group: pg.sprite.Group
    
    sprite_group: list

    tick: int

    def __init__(self, sio) -> None:
        self.sio = sio
        self.draw_properties = {
            'sprites': [],
            'map': c.MAP
        }

        self.enemy_index = {}
        for enemy in os.listdir('enemy'):
            if os.path.isfile(os.path.join('enemy', enemy)): continue
            spec = importlib.util.find_spec(f"enemy.{enemy}.behavior")
            lib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lib)
            
            behavior = getattr(lib, enemy)
            if behavior:
                self.enemy_index[enemy] = behavior
                print(f"Enemy {enemy} loaded!")
            else:
                print(f"Enemy {enemy} failed: behavior not found")

            
        self.lives = 69

        self.clock = pg.time.Clock()
        self.tick = 0
        
        self.sprite_group = []

        self.tower_group = pg.sprite.Group()
        self.projectile_group = pg.sprite.Group()

        self.enemy_group = pg.sprite.Group()
        self.enemy_downed = pg.sprite.Group()

    def on_mousedown(self, sid, pos):
        print("SHOOT!")
        self.shoot_test(pos)

    def start(self):
        self.run = True
        self.testcube = 1

        while self.run:
            self.update()

            self.testcube -= 1
            if self.testcube == 0:
                e = self.enemy_index[random.choice(['TriBede', 'Gura'])](self, self._random_waypoints())
                self.enemy_group.add(e)
                self.testcube = 30
            
            self.tick += 1
            self.sio.sleep(0.0333)


    def _random_waypoints(self):
        f = random.random()
        waypoints = []
        for i in behavior.waypoints:
            s = pg.Vector2(i[0])
            e = pg.Vector2(i[1])
            delta = (e-s)
            waypoints.append(s+ delta.normalize() * (f * delta.length()))
        return waypoints

    
    def shoot_test(self, pos: tuple[int] | pg.Vector2):
        pos = pg.Vector2(pos)
        if len(self.enemy_group)==0: target = pg.Vector2()
        else: target = pg.Vector2(min(self.enemy_group, key=lambda x: (x.pos-pos).length()).rect.center)
        movement = target - pos

        bullet = self.index['projectile'][random.choice(['rock_1', 'rock_2'])](self, pos, movement)
        self.projectile_group.add(bullet)
    
    def update(self):
        self.tower_group.update()
        self.projectile_group.update()
        
        self.enemy_group.update()
        self.enemy_downed.update()

        # sos
        self.sprite_group = self.enemy_group.sprites() + self.tower_group.sprites() + self.projectile_group.sprites() + self.enemy_downed.sprites()
        self.sprite_group.sort(key=lambda x: x.pos[1], reverse=True)

        sprites = []
        for i in self.sprite_group:
            sprites.append(i.draw_properties())
        
        self.draw_properties['sprites'] = sprites

