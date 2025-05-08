from multiprocessing.managers import BaseManager

class Counter:
    _counters = {}

    def __init__(self, name: str=None):
        if not name or not isinstance(name, str) or len(name) == 0: 
            raise ValueError("Counter name must be a non-empty string.")
        self.name = name
        Counter._counters.setdefault(self.name, 0)
    
    def value(self):
        return Counter._counters.get(self.name, 0)
    
    def increment(self):
        Counter._counters[self.name] += 1
        return Counter._counters[self.name]
    
    def set(self, value):
        if not isinstance(value, int):
            self.increment()
        Counter._counters[self.name] = value
        return Counter._counters[self.name]


# Manager server class.
class Server(BaseManager): pass

Server.register("Counter", Counter)

# Creates and run a server instance.
server = Server(address=('', 55555), authkey=b"1Belgisches4tel23")
server.get_server().serve_forever()