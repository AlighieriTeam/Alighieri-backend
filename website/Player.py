class Player:
    def __init__(self, id, name, points=0, creator=False):
        self.id = id
        self.name = name
        self.points = points
        self.creator = creator
