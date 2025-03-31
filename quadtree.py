"""
Quadtree implementation
"""

from numpy import log2

class node:
    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.pos_x = pos[0] # horizontal relative position
        self.pos_y = pos[1] # vertical relative position

        self.center: tuple[float, float] = (pos[0] + size[0]/2, pos[1] + size[1]/2)
        self.size = size


class quadTree:

    def __init__(self,
        start_pos: tuple[float, float] = (0, 0),
        size: tuple[float, float] = (1600, 900),
        max_deep: int = None
    ):
        self.root: node = node(start_pos, size)
        self.len: int = 0
        self.deep: int = 0
        self.max_deep = max_deep if max_deep is not None else int(log2(min(size)))

        self._node_0: node = None
        self._node_1: node = None
        self._node_2: node = None
        self._node_3: node = None

    def __repr__(self):
        return f"<quadTree len:{self.len}, deep:{self.deep}, max-deep:{self.max_deep}>"

    def __len__(self):
        return self.len

    def put(self):
        pass

    def search(self):
        pass