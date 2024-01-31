import random
import time
import math
import matplotlib.pyplot as plt
from collections import defaultdict

from structure_learning import Samples, Heuristic, LogaritmicHeuristic, k2
from structure_learning.networks import read_net_file

net = read_net_file("assets/insurance.net")

LIMIT = 10
diffs = []
times = []
num_samples = [1000 * (2**i) for i in range(8)]

nodes_order = list(net.nodes.values())
for num_sample in num_samples:
    sample = Samples(net, num_sample)
    h = LogaritmicHeuristic(sample)
    h.compute_factorials()
    start = time.time()
    n = k2(nodes_order, h, LIMIT)
    end = time.time()
    times.append(end - start)
    diffs.append(net.count_diff_colliders(n))

    print(f"sample:{len(sample.data)} diff:{diffs[-1]} time:{times[-1]}")
    if diffs[-1][0] == 0 and diffs[-1][1] == 0:
        break

fig, ax = plt.subplots(layout="constrained")

ax.plot(
    num_samples,
    [add for add, _ in diffs],
    label=f"Additions",
    color="green",
)
ax.plot(
    num_samples,
    [rem for _, rem in diffs],
    label=f"Deletions",
    color="red",
)
ax2 = ax.twinx()
ax2.plot(
    num_samples,
    times,
    color="blue",
    linestyle="dotted",
)


ax.legend()
ax.set_ylabel("# Additions/Deletions")
ax2.set_ylabel("Time (s)", color="b")
ax.set_xlabel("Samples")

plt.savefig(f"assets/plots/graph_min_diff.png", dpi=300)
