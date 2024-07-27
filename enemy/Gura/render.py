import os
import pygame as pg


gura_1 = pg.image.load(os.path.join('enemy', 'Gura', 'gura_1.png')).convert_alpha()
gura_sit = pg.image.load(os.path.join('enemy', 'Gura', 'gura_sit.png')).convert_alpha()
gura_death1 = pg.image.load(os.path.join('enemy', 'Gura', 'gura_death1.png')).convert_alpha()
gura_death2 = pg.image.load(os.path.join('enemy', 'Gura', 'gura_death2.png')).convert_alpha()

def render(properties: dict, screen: pg.Surface) -> None:
    if not properties['delta'].get('death'): render_alive(properties, screen)
    else: render_dead(properties, screen)

def render_alive(properties: dict, screen: pg.Surface) -> None:
    if properties['delta']['spawn']%600 < 300: surf = gura_1
    else: surf=gura_sit

    surf = pg.transform.flip(surf, properties['movement'][0]<0, False)
    screen.blit(surf, surf.get_rect(midbottom = properties['pos']))


def render_dead(properties: dict, screen: pg.Surface) -> None:
    delta = properties['delta']['death']
    if delta < 15: surf = gura_death1
    else: surf = gura_death2

    surf = pg.transform.flip(surf, properties['movement'][0]<0, False)
    screen.blit(surf, surf.get_rect(midbottom = properties['pos']))

