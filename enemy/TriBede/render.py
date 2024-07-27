import os, server.engine as engine
import pygame as pg
import random


TriAnimation = [pg.image.load(os.path.join('enemy', 'TriBede', f'CT{i}.png')).convert_alpha() for i in range(1, 6)]
graveyard = pg.image.load(os.path.join('enemy', 'graveyard.png')).convert_alpha()

def render(properties: dict, screen: pg.Surface) -> None:
    if not properties['delta'].get('death'): render_alive(properties, screen)
    else: render_dead(properties, screen)

def render_alive(properties: dict, screen: pg.Surface) -> dict:
    surf = random.choice(TriAnimation)
    surf = pg.transform.flip(surf, properties['movement'][0]<0, False)
    screen.blit(surf, surf.get_rect(midbottom = properties['pos']))

def render_dead(properties: dict, screen: pg.Surface):
    surf = graveyard
    surf = pg.transform.flip(surf, properties['movement'][0]<0, False)
    screen.blit(surf, surf.get_rect(midbottom = properties['pos']))

