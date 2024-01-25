import math
from collections import defaultdict

from .networks import CPTBayesianNode
from .samples import Samples


class Heuristic:
    def __init__(self, samples: Samples):
        self.samples = samples
        self.factorials = []

    def check_factorials(self):
        if len(self.factorials) > 0:
            return
        self.compute_factorials()

    def compute_factorials(self):
        self.factorials = [1]
        current_fact = 1
        for i in range(
            1, len(self.samples.data) + max(len(n.values) for n in self.samples.nodes)
        ):
            current_fact *= i
            self.factorials.append(current_fact)

    def compute_score(
        self, node: CPTBayesianNode, parents: list[CPTBayesianNode]
    ) -> float:
        score = 1
        parent_assignments = defaultdict(lambda: 0)
        node_assignments = defaultdict(lambda: 0)
        for sample in self.samples.data:
            assignment = tuple(sample[p] for p in parents)
            parent_assignments[assignment] += 1
            node_assignments[assignment + (sample[node],)] += 1
        for p_assignment, p_count in parent_assignments.items():
            score *= (
                self.factorials[len(node.values) - 1]
                / self.factorials[p_count + len(node.values) - 1]
            )
            for v in node.values:
                score *= self.factorials[node_assignments[p_assignment + (v,)]]
        return score

    def score(self, node: CPTBayesianNode, parents: list[CPTBayesianNode]) -> float:
        self.check_factorials()
        return self.compute_score(node, parents)


class LogaritmicHeuristic(Heuristic):
    def compute_factorials(self):
        self.factorials = [0]
        current_fact = 0
        for i in range(
            1, len(self.samples.data) + max(len(n.values) for n in self.samples.nodes)
        ):
            current_fact += math.log(i)
            self.factorials.append(current_fact)

    def compute_score(
        self, node: CPTBayesianNode, parents: list[CPTBayesianNode]
    ) -> float:
        score = 0
        parent_assignments = defaultdict(lambda: 0)
        node_assignments = defaultdict(lambda: 0)
        for sample in self.samples.data:
            assignment = tuple(sample[p] for p in parents)
            parent_assignments[assignment] += 1
            node_assignments[assignment + (sample[node],)] += 1
        for p_assignment, p_count in parent_assignments.items():
            score += (
                self.factorials[len(node.values) - 1]
                - self.factorials[p_count + len(node.values) - 1]
            )
            for v in node.values:
                score += self.factorials[node_assignments[p_assignment + (v,)]]
        return score
