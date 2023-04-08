import sys
from typing import List, Set, Dict


class Vertex:
    __match_args__ = ("__id", "__value")

    def __init__(self, vertex_id: int) -> 'Vertex':
        self.__id = vertex_id
        self.__value = vertex_id

    def get_value(self) -> int:
        return self.__value

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.__id) + "(" + str(self.__value) + ")"

    def __eq__(self, other: 'Vertex') -> bool:
        return self.__id == other.__id

    def __hash__(self) -> int:
        return hash(self.__id)

    def __iter__(self):
        return iter((self.__id, self.__value))


class Edge:
    def __init__(self, from_vert: Vertex, to_vert: Vertex, weight=None) -> 'Edge':
        self.__from = from_vert
        self.__to = to_vert
        self.__weight = weight

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.__from) + " -> " + str(self.__to)

    def __eq__(self, other: 'Vertex') -> bool:
        return self.__from == other.__from and self.__to == other.__to

    def __hash__(self) -> int:
        return hash(self.__from) + hash(self.__to)

    def __iter__(self):
        if self.__weight:
            return iter((self.__from, self.__to, self.__weight))

        return iter((self.__from, self.__to))


class PregelEdge(Edge):
    def __init__(self, from_vert: 'PregelVertex', to_vert: 'PregelVertex') -> 'PregelEdge':
        super().__init__(from_vert, to_vert)


class PregelManager:
    def __init__(self, graph: Set['PregelEdge'], initial_message: int = sys.maxsize) -> 'PregelManager':
        self.__messages: Dict['PregelVertex', List[int]] = dict()
        self.__next_superstep_messages: Dict['PregelVertex', List[int]] = dict()
        self.__graph = graph

        for src, dst in graph:
            self.__messages[src] = [ src.get_value() ]
            self.__messages[dst] = [ dst.get_value() ]

    def notify_neighbours(self, vertex: 'PregelVertex', value: int) -> None:
        for from_vertex, to_vertex in self.__graph:
            if from_vertex != vertex: continue
            if to_vertex in self.__next_superstep_messages:
                self.__next_superstep_messages[to_vertex].append(value)
            else:
                self.__next_superstep_messages[to_vertex] = [value]

    def get_messages(self, vertex: 'PregelVertex') -> List[int]:
        if vertex not in self.__messages: return []
        return self.__messages[vertex]

    def superstep(self) -> None:
        self.__messages = {k: v for k, v in self.__next_superstep_messages.items()}
        self.__next_superstep_messages = dict()

    def has_next(self) -> bool:
        return len(self.__messages) > 0

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.__next_superstep_messages) + str(self.__messages)


class PregelVertex(Vertex):
    def __init__(self, vertex_id: int) -> 'PregelVertex':
        super().__init__(vertex_id)

    def compute(self, manager: PregelManager) -> None:
        messages: List[int] = manager.get_messages(self)

        if not messages: return

        if self._Vertex__value >= (min_value := min(messages)):
            self._Vertex__value = min_value
            manager.notify_neighbours(self, self._Vertex__value)


def init_graph() -> Set[PregelEdge]:
    one = PregelVertex(1)
    two = PregelVertex(2)
    three = PregelVertex(3)
    four = PregelVertex(4)
    five = PregelVertex(5)
    six = PregelVertex(6)

    return {
        PregelEdge(one, two),
        PregelEdge(one, three),
        PregelEdge(two, three),

        PregelEdge(four, five),

        PregelEdge(six, six)
    }


if __name__ == "__main__":
    graph = init_graph()
    manager = PregelManager(graph)

    while manager.has_next():
        for src, dst in graph:
            if src == dst: continue
            src.compute(manager)
            dst.compute(manager)
        manager.superstep()
    print(graph)
