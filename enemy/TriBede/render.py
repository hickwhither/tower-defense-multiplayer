import os, server.engine as engine
import pygame as pg
import random


TriAnimation = [pg.image.load(os.path.join('enemy', 'TriBede', f'CT{i}.png')).convert_alpha() for i in range(1, 6)]

def render(properties: dict, screen: pg.Surface) -> dict:
    surf = random.choice(TriAnimation)

    surf = pg.transform.flip(surf, properties['movement'][0]<0, False)
    screen.blit(surf, surf.get_rect(midbottom = properties['pos']))

