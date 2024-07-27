from client.clientsocketio import ClientSocketio
import constants_client as c

import os, importlib.util
import pygame as pg

import json
import os, sys

class Client:
    run: bool
    
    render: dict[dict]

    def __init__(self):
        pg.init()
        pg.display.set_caption("su beo")
        self.screen = pg.display.set_mode(c.SCREEN_RESOLUTION)
        self.clock = pg.time.Clock()
        self.sio = ClientSocketio()
        
        self.render = {}

        for type in ['enemy', 'map', 'projectile']:
            self.render[type] = {}
            for i in os.listdir(type):
                if os.path.isfile(os.path.join(type,i)): continue
                spec = importlib.util.find_spec(f"{type}.{i}.render")
                lib = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(lib)

                self.render[type][i] = lib


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

            self.screen.blit(self.render['map'][map].image, (0, 0))

            for i in sprites:
                self.render[i['type']][i['name']].render(i, self.screen)
                

            pg.display.update()
            self.clock.tick(c.FPS)
        
        pg.quit()
        exit()




