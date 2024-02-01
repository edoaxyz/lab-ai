import graphviz as gv
from typing import Self


class BayesianNode:
    def __init__(self, name: str, parents: list[Self] = []):
        self._childs = []
        self.name = name
        self.parents = []
        self.depth = 0
        for parent in parents:
            self.add_parent(parent)

    def __repr__(self) -> str:
        return self.name

    @property
    def childs(self) -> list[Self]:
        return self._childs

    def add_parent(self, parent: Self) -> None:
        self.parents.append(parent)
        self.depth = max(parent.depth + 1, self.depth)
        parent._childs.append(self)


class BayesianNetwork:
    def __init__(self, nodes: list[BayesianNode]):
        self.nodes = {node.name: node for node in nodes}

    @property
    def root_nodes(self) -> list[BayesianNode]:
        return [node for node in self.nodes.values() if not node.parents]

    def _check_equal_nodes(self, net: Self) -> bool:
        if any(n.name not in self.nodes for n in net.nodes.values()):
            return False
        return True

    def _get_links(self, net: Self) -> tuple[dict[BayesianNode, BayesianNode]]:
        if not self._check_equal_nodes(net):
            raise ValueError("The networks must have same nodes' names")
        links = {node: net.nodes[node.name] for node in self.nodes.values()}
        reversed_links = {v: k for k, v in links.items()}
        return links, reversed_links

    def get_colliders(self) -> set[BayesianNode]:
        colliders = set()
        for node in self.nodes.values():
            if len(node.parents) > 1:
                colliders.add(node)
        return colliders

    def count_diff_colliders(self, net: Self) -> tuple[int, int]:
        _, rev_links = self._get_links(net)
        colliders = self.get_colliders()
        net_colliders = {rev_links[coll] for coll in net.get_colliders()}
        return (
            len(net_colliders - colliders),  # added
            len(colliders - net_colliders),  # removed
        )

    def draw_graph(self, filename: str) -> None:
        graph = gv.Digraph()
        colliders = self.get_colliders()
        for node in self.nodes.values():
            graph.node(node.name, color="red" if node in colliders else "black")
            for child in node.childs:
                graph.edge(node.name, child.name)
        graph.render(filename=filename, format="png", cleanup=True)
