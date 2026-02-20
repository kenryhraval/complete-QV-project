import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 

def plot_qv_summary(results):
    plt.figure(figsize=(7,5))

    for backend_name, backend_results in results.items():
        Ns = sorted(backend_results.keys())
        final_hops = [backend_results[N]["cumulative_hops"][-1] for N in Ns]
        
        errors = [np.sqrt(h * (1.0 - h) / k) for h in final_hops]

        plt.errorbar(
            Ns, 
            final_hops, 
            yerr=2 * np.array(errors),
            marker='o', 
            capsize=4, 
            label=backend_name
        )

    plt.axhline(2/3, color='black', linestyle='--', linewidth=1, label="Slieksnis $2/3$")
    plt.xlabel("Kubitu skaits un ķēdes dziļums")
    plt.ylabel("Heavy output varbūtība")
    plt.title("Kvantu tilpuma eksperiments uz vairākām iekārtām")
    plt.ylim(0.4, 1.0)
    plt.xticks(range(2, max(max(r.keys()) for r in results.values())+1))
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()


def plot_qv_probability(results):
    plt.figure(figsize=(7, 5))

    for backend_name, backend_results in results.items():
        Ns = sorted(backend_results.keys())
        probs = []

        for N in Ns:
            h = backend_results[N]["cumulative_hops"][-1]

            se = np.sqrt(h * (1 - h) / k)
            z = (h - 2/3) / se
            p = norm.cdf(z) 

            probs.append(p)

        plt.plot(Ns, probs, marker='o', label=backend_name)

    p_thresh = norm.cdf(2)
    plt.axhline(p_thresh, linestyle='--', linewidth=1, label="$0.975$")

    plt.xlabel("Kubitu skaits un ķēdes dziļums $N$")
    plt.ylabel(r"Ticamība $P(HOP_{vid} > 2/3)$")
    plt.title("Ticamība, ka QV ir sasniegts")
    plt.ylim(0.0, 1.05)

    max_N = max(max(r.keys()) for r in results.values())
    plt.xticks(range(2, max_N + 1))

    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()