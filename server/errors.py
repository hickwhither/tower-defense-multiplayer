
class IndexAlreadyLoaded(Exception):
    """Index is already loaded"""
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def __repr__(self): return f"`{self.name}` already imported in `{self.type}`"


class TypeNotFound(Exception):
    """If that type doesn't exists"""
    def __init__(self, type): self.type = type
    def __repr__(self): return f"`{self.type}` not found boo"
