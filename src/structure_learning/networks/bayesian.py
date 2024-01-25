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

    def get_diff_deps(self, net: Self) -> dict[BayesianNode, tuple[int, int]]:
        links, rev_links = self._get_links(net)
        return {
            node: (
                sum(
                    1
                    for child in links[node].childs
                    if rev_links[child] not in node.childs
                ),  # added
                sum(
                    1 for child in node.childs if links[child] not in links[node].childs
                ),  # removed
            )
            for node in self.nodes.values()
        }

    def count_diff_deps(self, net: Self) -> tuple[int, int]:
        diffs = self.get_diff_deps(net)
        return (
            sum(added for added, _ in diffs.values()),
            sum(removed for _, removed in diffs.values()),
        )

    def draw_graph(self, filename: str) -> None:
        graph = gv.Digraph()
        for node in self.nodes.values():
            graph.node(node.name)
            for child in node.childs:
                graph.edge(node.name, child.name)
        graph.render(filename=filename, format="png", cleanup=True)
