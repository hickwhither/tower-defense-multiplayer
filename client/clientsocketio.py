import socketio

class ClientSocketio(socketio.Client):

    def __init__(self):
        super().__init__()
        self.on('connect', self.on_connect)
        self.event('disconnect', self.on_disconnect)
    
    def connect_to(self, ip_address):
        self.connect(ip_address)
    
    def on_connect(self):
        print('connection established')

    def on_disconnect(self):
        print('disconnected from server')
    
