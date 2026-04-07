import rustworkx as rx

def connected_subsets(coupling_map, n: int):
    """
    Returns list of n-tuples (sorted tuples) that are 
    connected (induced subgraph is connected).
    """

    nodes = sorted({int(a) for a, _ in coupling_map} | {int(b) for _, b in coupling_map})
    if n == 1:
        return [(q,) for q in nodes]
    if len(nodes) < n:
        return []

    # build mapping: qubit label -> rustworkx node index
    g = rx.PyGraph(multigraph=False)
    label_to_idx = {}
    for q in nodes:
        label_to_idx[q] = g.add_node(q)  # store the label as node payload

    # add edges
    for a, b in coupling_map:
        a = int(a); b = int(b)
        g.add_edge(label_to_idx[a], label_to_idx[b], None)

    # enumerate connected k-node subgraphs (returns lists of node indices)
    subgraphs = rx.connected_subgraphs(g, n)

    # convert node indices back to qubit labels (payloads), sort each tuple
    out = []
    for idxs in subgraphs:
        labels = sorted(g[idx] for idx in idxs)
        out.append(tuple(labels))

    # ensure uniqueness + deterministic ordering
    return sorted(set(out))

