import random
from typing import Self

from .bayesian import BayesianNetwork, BayesianNode


class CPTBayesianNode(BayesianNode):
    def __init__(
        self,
        name: str,
        values: list[str],
        probabilities: list,
        parents: list[Self] = [],
    ):
        super().__init__(name, parents)
        self.values = values
        self.probabilities = probabilities
        self.calculate_cpt()

    def calculate_cpt(self) -> None:
        nodes = self.parents + [self]
        combinations = {
            (val,): self.probabilities[i] for i, val in enumerate(nodes[0].values)
        }
        for parent in nodes[1:]:
            combinations = {
                combination + (val,): probs[i]
                for i, val in enumerate(parent.values)
                for combination, probs in combinations.items()
            }
        self.cpt = combinations
        self.cpt_nodes = {node: i for i, node in enumerate(nodes)}

    def get_random_value(self, assignment: dict) -> str:
        if any(parent not in assignment.keys() for parent in self.parents):
            return None

        cpt_key = tuple(
            assignment[k]
            for k in sorted(
                set(assignment.keys()).intersection(self.cpt_nodes.keys()),
                key=lambda node: self.cpt_nodes[node],
            )
        )
        random_value = random.random()
        curr_prob = 0
        for value in self.values:
            prob = self.cpt[cpt_key + (value,)]
            if random_value < curr_prob + prob and random_value >= curr_prob:
                return value
            curr_prob += prob


class CPTBayesianNetwork(BayesianNetwork):
    def __init__(self, nodes: list[CPTBayesianNode]):
        super().__init__(nodes)

    def generate_random_sample(self) -> dict[CPTBayesianNode, str]:
        nodes = self.root_nodes
        assignment = {}
        while len(nodes) > 0:
            node = nodes.pop(0)
            if node in assignment:
                continue
            value = node.get_random_value(assignment)
            if value is None:
                nodes.append(node)
            else:
                assignment[node] = value
                nodes.extend(node.childs)
        return assignment
