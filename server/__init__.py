import socketio, eventlet

from .engine import Engine
import constants_server as c

class ServerSocketio(socketio.Server):
    engine: Engine

    def __init__(self):
        super().__init__()
        self.engine = Engine(self)

        self.app = socketio.WSGIApp(self)
        self.on('connect', self.on_connect)
        self.on('disconnect', self.on_disconnect)
        self.event(self.on_mousedown)
        self.event(self.draw_properties)
    
    def start(self):
        bg_task = self.start_background_task(self.engine.start)
        eventlet.wsgi.server(eventlet.listen((c.HOST, c.PORT)), self.app)

    def on_connect(self, sid, environ):
        print(f'connect {sid}')
    
    def on_disconnect(self, sid):
        print(f'disconnect {sid}')
    
    def on_mousedown(self, sid, data):
        self.engine.on_mousedown(sid, data['mouse_pos'])
    
    def draw_properties(self, sid):
        return self.engine.draw_properties

