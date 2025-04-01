"""
Quadtree implementation
"""

import numpy as np


class node:
    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.has_item: bool = False
        self.pos = pos # 0:horizontal, 1:vertical relative positions
        # self.center: tuple[float, float] = (pos[0] + size[0]/2, pos[1] + size[1]/2)
        self.size = size

    def __contains__(self, pos: tuple[float, float]) -> bool:
        if (pos[0] < self.pos[0]) or (pos[0] > self.pos[0] + self.size[0]):
            return False

        if (pos[1] < self.pos[1]) or (pos[1] > self.pos[1] + self.size[1]):
            return False

        return True


class quadTree:

    def __init__(self,
        boundaries: tuple[float, float],
        start_pos: tuple[float, float],
        max_deep: int = None,
    ):
        self.boundaries = boundaries
        self.root = node(start_pos, boundaries)
        self.len: int = 0
        self.max_deep = max_deep

        if (max_deep is None):
            self.max_deep = int(np.log2(min(boundaries)))

        self._node_0: quadTree = None
        self._node_1: quadTree = None
        self._node_2: quadTree = None
        self._node_3: quadTree = None

        self._stack: list[quadTree] = [self]

    def __repr__(self):
        return f"<quadTree len:{self.len}, max-deep:{self.max_deep}>"

    def __len__(self):
        assert self._node_0.len + self._node_1.len + self._node_2.len + self._node_3.len == self.len
        return self.len

    def __iter__(self):
        self._stack = [self]  # Reset stack for new iteration
        return self

    def __next__(self):
        if not self._stack:
            raise StopIteration

        sub_tree = self._stack.pop()

        # Push children to the stack if they exist
        nodes = (sub_tree._node_0, sub_tree._node_1, sub_tree._node_2, sub_tree._node_3)
        for child in nodes:
            if child is not None:
                self._stack.append(child)

        # Yield the current node
        return sub_tree

    def create_nodes(self):
        # node0 | node1
        # ------+------
        # node2 | node3
        half_bound = (self.boundaries[0]/2, self.boundaries[1]/2)
        sum_at_x = self.root.pos[0] + half_bound[0]
        sum_at_y = self.root.pos[1] + half_bound[1]

        self._node_0 = quadTree(half_bound, self.root.pos, self.max_deep-1)
        self._node_1 = quadTree(half_bound, (sum_at_x, self.root.pos[1]), self.max_deep-1)
        self._node_2 = quadTree(half_bound, (self.root.pos[0], sum_at_y), self.max_deep-1)
        self._node_3 = quadTree(half_bound, (sum_at_x, sum_at_y), self.max_deep-1)

    def put(self, pos: tuple[float, float]) -> None:
        if not pos in self.root:
            raise Exception(f"This position ({pos}), it is out of boundaries.")

        self.__put(pos, level=0)
        self.len += 1
        return None

    def __put(self, pos: tuple[float, float], level: int,) -> None:
        half_bound = (self.boundaries[0]/2, self.boundaries[1]/2)

        # if next boundaries are less than 1 or it is at the maximun resolution, then stop and insert
        if (min(half_bound)/2 <= 1) or (level == self.max_deep):
            self.root = node(pos, half_bound)
            self.len += 1
            return None

        if self._node_0 is None:
            self.create_nodes()

        if pos in self._node_0.root:
            self._node_0.__put(pos, level+1)
            self._node_0.len += 1
            return None

        elif pos in self._node_1.root:
            self._node_1.__put(pos, level+1)
            self._node_1.len += 1
            return None

        elif pos in self._node_2.root:
            self._node_2.__put(pos, level+1)
            self._node_2.len += 1
            return None

        elif pos in self._node_3.root:
            self._node_3.__put(pos, level+1)
            self._node_3.len += 1
            return None

        print("Que merda aconteceu aqui??\nPos:", pos, "Level:", level)
        return None

    def search(self):
        pass
