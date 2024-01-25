from .networks import CPTBayesianNode, BayesianNode, BayesianNetwork
from .heuristics import Heuristic


def k2(
    nodes: list[CPTBayesianNode], heuristic: Heuristic, max_parents: int
) -> BayesianNetwork:
    new_nodes = {node.name: BayesianNode(node.name, []) for node in nodes}
    network_score = 0
    for i, node in enumerate(nodes):
        parents = set()
        score = heuristic.score(node, parents)
        ok_to_proceed = True
        while ok_to_proceed and len(parents) < max_parents:
            best_score = float("-inf")
            best_parent = None
            for n in nodes[:i]:
                if n in parents:
                    continue
                new_score = heuristic.score(node, [*parents, n])
                if new_score > best_score:
                    best_score = new_score
                    best_parent = n
            if best_score > score:
                score = best_score
                parents.add(best_parent)
            else:
                ok_to_proceed = False
        for p in parents:
            new_nodes[node.name].add_parent(new_nodes[p.name])
        network_score += score
    return BayesianNetwork(new_nodes.values()), network_score
