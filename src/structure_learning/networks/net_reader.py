import re

from .cpt_bayesian import CPTBayesianNetwork, CPTBayesianNode


def _parse_list(string: str) -> list:
    string = string.strip()
    level = 0
    start = -1
    data = []
    for i, char in enumerate(string):
        check = False
        if char == "(":
            if level == 0:
                start = i
            level += 1
        elif char == ")":
            level -= 1
            if level == 0:
                data.append(_parse_list(string[start + 1 : i]))
    if len(data) == 0:
        return [float(v) for v in string.split()]
    return data


def read_net_file(filename: str) -> CPTBayesianNetwork:
    with open(filename, "r") as file:
        lines = file.readlines()
    nodes = {}
    potentials = {}

    current_node = None
    current_potential = None

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("node"):
            current_node = re.match(r"node (\w+)", line).group(1)
            nodes[current_node] = {"states": []}

        elif line.startswith("potential"):
            pot = re.match(r"potential \((.*?)\)", line).group(1).split("|")
            current_potential = pot[0].strip()
            potentials[current_potential] = {
                "data": [],
                "parents": pot[1].strip().split() if len(pot) > 1 else [],
            }

        elif line.startswith("states"):
            states = re.match(r"states = \((.*?)\) *;", line).group(1)
            nodes[current_node]["states"] = states.replace('"', "").split()

        elif line.startswith("data"):
            data = "(" + re.match(r"data = \((.*?)\) *;", line).group(1) + ")"
            potentials[current_potential]["data"] = _parse_list(data)[0]

    order = []
    queue = list(nodes.keys())
    while len(queue) > 0:
        n = queue.pop(0)
        if all(p in order for p in potentials[n]["parents"]):
            order.append(n)
        else:
            queue.append(n)

    node_list = {}
    for n in order:
        node_list[n] = CPTBayesianNode(
            n,
            nodes[n]["states"],
            potentials[n]["data"],
            [node_list[p] for p in potentials[n]["parents"]],
        )

    return CPTBayesianNetwork(list(node_list.values()))
