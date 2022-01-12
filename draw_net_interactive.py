
import networkx as nx

from pyvis import network as net


def plot_interactive(G: nx.Graph, graph_size=800, spatial_position=None, communities=None, labels=True,weight="weight", node_size=2,
                     title=None):
    """

    Parameters
    ----------
    G
    graph_size
    spatial_position
    communities: name of attribute or dictionary
    weight
    color
    title

    Returns
    -------

    """

    # copy without attributes
    Gcopy = nx.Graph()
    Gcopy.add_edges_from((u, v) for u, v in G.edges())
    Gcopy.add_nodes_from(u for u in G.nodes())

    # initialize basic nodes and edges titles
    titles_nodes = {n: str(n) + "\n" for n in G.nodes()}
    titles_edges = {e: str(e) + "\n" for e in G.edges()}

    if communities is not None:
        if isinstance(communities, str):
            communities = nx.get_node_attributes(G, communities)

        nx.set_node_attributes(Gcopy, {n: int(b) for n, b in communities.items()}, "group")
        for n in titles_nodes:
            titles_nodes[n] += " </br>group: " + str(communities[n])

    if spatial_position is not None:
        if isinstance(spatial_position, str):
            spatial_position = nx.get_node_attributes(G, spatial_position)
        elif isinstance(spatial_position, list) and len(spatial_position) == 2:
            x_values = nx.get_node_attributes(G, spatial_position[0])
            y_values = nx.get_node_attributes(G, spatial_position[1])
            spatial_position={n:(x_values[n],y_values[n]) for n in x_values.keys()}

        x_values = {i for k, (i, j) in spatial_position.items()}
        y_values = {j for k, (i, j) in spatial_position.items()}
        min_x = min(x_values)
        max_x = max(x_values)

        min_y = min(y_values)
        max_y = max(y_values)
        range_x = max_x - min_x
        range_y = max_y - min_y

        nx.set_node_attributes(Gcopy, {k: (float(i) - min_x) / range_x * 500 * 0.9 for k, (i, j) in spatial_position.items()}, "x")
        nx.set_node_attributes(Gcopy, {k: -1 * (float(j) - min_y) / range_y * 500 * 0.9 for k, (i, j) in spatial_position.items()},
                               "y")
        for n in Gcopy.nodes:
            titles_nodes[n] = titles_nodes[n] + "</br>(x,y):" + str(spatial_position[n][0]) + "," + str(spatial_position[n][1]) + "\n"

    if (labels==False):
        nx.set_node_attributes(Gcopy,{n:" " for n in Gcopy.nodes},"label")
    print(Gcopy.nodes[0])
    nx.set_node_attributes(Gcopy, titles_nodes, "title")
    nx.set_edge_attributes(Gcopy, titles_edges, "title")

    # print(Gcopy.nodes[1])
    to_plot = net.Network(str(graph_size) + "px", str(graph_size) + "px", notebook=True)
    to_plot.from_nx(Gcopy, default_node_size=node_size)
    to_plot.inherit_edge_colors(False)
    if spatial_position is not None:
        to_plot.toggle_physics(False)
        # for n in to_plot.nodes:
        #    n.update({'physics': False})
    # to_plot.inherit_edge_colors(False)
    return (to_plot)

