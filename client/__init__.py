from client.clientsocketio import ClientSocketio
import constants_client as c

import os, importlib.util
import pygame as pg

import json
import os, sys

class Client:
    run: bool
        

    def __init__(self):
        pg.init()
        pg.display.set_caption("su beo")
        self.screen = pg.display.set_mode(c.SCREEN_RESOLUTION)
        self.clock = pg.time.Clock()
        self.sio = ClientSocketio()
        
        self.enemy_render = {}
        for enemy in os.listdir('enemy'):
            if os.path.isfile(os.path.join('enemy',enemy)): continue
            spec = importlib.util.find_spec(f"enemy.{enemy}.render")
            lib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lib)

            self.enemy_render[enemy] = lib
        
        self.map_render = {}
        for map in os.listdir('map'):
            if os.path.isfile(os.path.join('map', map)): continue
            spec = importlib.util.find_spec(f"map.{map}.render")
            lib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lib)

            self.map_render[map] = lib


    def start(self):
        self.run = True
        self.sio.connect_to(c.CONNECT_URL)

        while self.run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.run = False
                    self.sio.disconnect()
                    return
                if e.type == pg.MOUSEBUTTONDOWN:
                    self.sio.emit('on_mousedown', {'mouse_pos': pg.mouse.get_pos()})
            
            draw_properties = self.sio.call('draw_properties')
            sprites = draw_properties['sprites']
            map = draw_properties['map']

            self.screen.blit(self.map_render[map].image, (0, 0))

            for i in sprites:
                if i['type'] != 'enemy': continue
                self.enemy_render[i['name']].render(i, self.screen)


            pg.display.update()
            self.clock.tick(c.FPS)
        
        pg.quit()
        exit()




