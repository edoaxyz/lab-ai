## Structure Learning for Bayesian networks

This project follows [this paper](https://link.springer.com/content/pdf/10.1007/BF00994110.pdf) to implement a structure learning algorithm known as *K2*. Tests on it are done using *Insurance* network from the [bnlearn package](https://www.bnlearn.com/bnrepository/discrete-medium.html#insurance).

### Repo structure

 - `src` contains the Python code
   - `assets` folder used for input and output files of Python scripts
   - `structure_learning` main Python module for structure learning
     - `networks` sub-module for Bayesian networks
       - `bayesian.py` Bayesian network classes (Node and Network)
       - `cpt_bayesian.py` Same classes as in `bayesian.py` but with conditional probability tables for savings *bnlearn*'s networks
       - `net_reader.py` Functions to read networks from `.net` files
     - `heuristics.py` Heuristics classes for K2 algorithm (Factorial Heuristic and Logarithmic Heuristic)
     - `k2.py` K2 algorithm implementation
     - `samples.py` Class for creating and managing samples from a Bayesian network with CPTs
   - `main_comparison.py` Script to compare K2 algorithm with different parameters and sample sizes
   - `min_diff.py` Script that tries to find the minimum colliders difference between a K2's generated network and the original network from *bnlearn*
 - `docs` contains LaTeX source files for documentation

### How to run

You might need to install Python 3.8, `pip`, `graphviz` and `gzip` for decompressing the bnlearn network. Then, run the following commands:

```bash
cd src
wget -O - https://www.bnlearn.com/bnrepository/insurance/insurance.net.gz  | gzip -d > assets/insurance.net
pip install -r requirements.txt
python main_comparison.py
python min_diff.py
```


