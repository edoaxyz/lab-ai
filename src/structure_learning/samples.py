from collections import defaultdict
from itertools import combinations

from .networks import CPTBayesianNetwork


class Samples:
    def __init__(self, network: CPTBayesianNetwork, n_samples: int):
        self.network = network
        self.nodes = list(network.nodes.values())
        self.data = [network.generate_random_sample() for _ in range(n_samples)]
