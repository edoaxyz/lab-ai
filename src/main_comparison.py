import random
import time
import math
import matplotlib.pyplot as plt
from collections import defaultdict

from structure_learning import Samples, Heuristic, LogaritmicHeuristic, k2
from structure_learning.networks import read_net_file

net = read_net_file("assets/insurance.net")

TIME_ROUNDS = 3
SAMPLES = [Samples(net, n) for n in range(20, 201, 20)]
LIMITS = [1, 2, 3, 5]
times = {
    Heuristic: {limit: [None] * len(SAMPLES) for limit in LIMITS},
    LogaritmicHeuristic: {limit: [None] * len(SAMPLES) for limit in LIMITS},
}
diffs = {
    Heuristic: {limit: [(None, None)] * len(SAMPLES) for limit in LIMITS},
    LogaritmicHeuristic: {limit: [(None, None)] * len(SAMPLES) for limit in LIMITS},
}


for r in range(TIME_ROUNDS):
    nodes_order = list(net.nodes.values())
    for i, sample in enumerate(SAMPLES):
        for heuristic in [Heuristic, LogaritmicHeuristic]:
            h = heuristic(sample)
            h.compute_factorials()
            for limit in LIMITS:
                try:
                    start = time.time()
                    n = k2(nodes_order, h, limit)
                    end = time.time()
                    if end - start < (times[heuristic][limit][i] or float("inf")):
                        times[heuristic][limit][i] = end - start

                    if r == 0:
                        diffs[heuristic][limit][i] = net.count_diff_colliders(n)
                        n.draw_graph(f"assets/graphs/k2_{heuristic.__name__}_{limit}_{i}")

                    print(
                        f"round:{r} with {heuristic.__name__} max parents:{limit} sample:{i} time:{end - start}"
                    )
                except OverflowError:
                    pass


for heuristic in [Heuristic, LogaritmicHeuristic]:
    for i, limit in enumerate(LIMITS):
        plt.plot(
            [len(s.data) for s in SAMPLES],
            times[heuristic][limit],
            label=f"{heuristic.__name__} {limit} Max Parents",
            color="red" if heuristic == LogaritmicHeuristic else "blue",
            marker=f"${limit}$",
            markersize=10,
            markeredgecolor="black",
            markeredgewidth=0.40,
        )

lines = plt.gca().get_lines()
l1 = plt.legend(
    [lines[i] for i in range(len(LIMITS))],
    [f"{i} Max Parents" for i in LIMITS],
    loc=2,
)
l2 = plt.legend(
    [lines[i] for i in [0, len(LIMITS)]],
    ["Factorial Heuristic", "Logarithmic Heuristic"],
    loc=4,
)
plt.gca().add_artist(l1)
plt.gca().add_artist(l2)
plt.xlabel("Samples")
plt.ylabel("Time (s)")
plt.title(f"K2 Time Comparison")
plt.savefig(f"assets/plots/k2_times.png", dpi=300)
plt.clf()

fig, ax = plt.subplots(
    1, 2, figsize=(12, 6), sharey=True, gridspec_kw={"wspace": 0, "hspace": 0}
)
for j, heuristic in enumerate([Heuristic, LogaritmicHeuristic]):
    for i, limit in enumerate(LIMITS):
        ax[j].plot(
            [len(s.data) for s in SAMPLES],
            [add for add, _ in diffs[heuristic][limit]],
            label=f"Additions {heuristic.__name__} {limit} Max Parents",
            color="green",
            marker=f"${limit}$",
            markersize=10,
            markeredgecolor="black",
            markeredgewidth=0.40,
        )
        ax[j].plot(
            [len(s.data) for s in SAMPLES],
            [de for _, de in diffs[heuristic][limit]],
            label=f"Deletions {heuristic.__name__} {limit} Max Parents",
            color="red",
            marker=f"${limit}$",
            markersize=10,
            markeredgecolor="black",
            markeredgewidth=0.40,
        )

    ax[j].set_title(
        f"{'Logarithmic' if heuristic == LogaritmicHeuristic else 'Factorial'} Heuristic"
    )
    ax[j].set_xlabel("Samples")
    ax[j].set_ylabel("Colliders Added/Deleted")
    ax[j].label_outer()


lines = ax[0].get_lines()
l1 = fig.legend(
    lines[:2],
    ["Additions", "Deletions"],
    loc="lower center",
    bbox_to_anchor=(0.5, -0.10),
    ncol=2,
)
l2 = fig.legend(
    [lines[i] for i in range(0, len(LIMITS) * 2, 2)],
    [f"{i} Max Parents" for i in LIMITS],
    loc="lower center",
    ncol=len(LIMITS),
    bbox_to_anchor=(0.5, -0.05),
)

fig.add_artist(l1)
fig.add_artist(l2)

fig.suptitle(f"Diff Colliders Comparison")
fig.savefig(f"assets/plots/diffs_deps.png", bbox_inches="tight", dpi=300)
