import os
import pygame as pg


img = pg.image.load(os.path.join('projectile', 'rock_1', 'rock_1.png')).convert_alpha()

def render(properties: dict, screen: pg.Surface) -> None:
    surf = img
    surf = pg.transform.flip(surf, properties['movement'][0]<0, False)
    surf = pg.transform.rotate(surf, pg.Vector2(properties['movement']).angle_to((0, -1)))
    screen.blit(surf, surf.get_rect(center = properties['pos']))
