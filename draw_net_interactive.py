import networkx as nx
from pyvis import network as net
from colormap import rgb2hex
from matplotlib import colors
import matplotlib.pyplot as plt

def plot_interactive(G: nx.Graph, graph_size=800, spatial_position=None, communities=None, labels=True,weight="weight", node_size=2,
                     title=None,node_color=None,directed=False,customizable=False,min_node_size=2,max_node_size=10):
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
    if directed:
        Gcopy=nx.DiGraph()
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

    if isinstance(node_size,str):
        node_attr=nx.get_node_attributes(G,node_size)
        max_attr = max(list(node_attr.values()))
        new_sizes ={k:max(min_node_size,v/max_attr*max_node_size) for k,v in node_attr.items()}
        nx.set_node_attributes(Gcopy,new_sizes,"size")
        
        
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

    if node_color is not None and node_color!="color":
        color_values = nx.get_node_attributes(G, node_color)

        centered0=False
        min_color = min(color_values.values())
        max_color= max(color_values.values())
        if min_color<0:
            colorpalette = plt.get_cmap("coolwarm")
            centered0 = True 
            offset = colors.TwoSlopeNorm(vcenter=0.,vmin=min_color,vmax=max_color)
        else:
            colorpalette = plt.get_cmap("magma")
            offset = colors.Normalize(vmin=min_color,vmax=max_color)

        # print("color",min_val,max_val)
        color_colors={}
        for k in color_values:
            theCol = colorpalette(offset(color_values[k]))

            color_colors[k] = rgb2hex(int(theCol[0] * 255), int(theCol[1] * 255), int(theCol[2] * 255))
    
        nx.set_node_attributes(Gcopy, color_colors, "color")
        for n in titles_nodes:
            titles_nodes[n] += " </br>"+node_color+": " + str(color_values[n])
            
    if node_color=="color":
        nx.set_node_attributes(Gcopy, nx.get_node_attributes(G,"color"), "color")
        
        
        #for u, v in titles_:
         #   titles_edges[(u, v)] = titles_edges[(u, v)] + str(G[u][v][color]) + "\n<br>"
    if (labels==False):
        nx.set_node_attributes(Gcopy,{n:" " for n in Gcopy.nodes},"label")
    nx.set_node_attributes(Gcopy, titles_nodes, "title")
    nx.set_edge_attributes(Gcopy, titles_edges, "title")
    
    arrows="false"
    if directed:
        arrows="true"
    options = """var options = {
      "edges": {
        "arrows": {
          "to": {
        "enabled": """+arrows+""",
        "scaleFactor": 0.15
          }
        }
        }
        }"""
        


        


            
    to_plot = net.Network(str(graph_size) + "px", str(graph_size) + "px", notebook=True)
    to_plot.from_nx(Gcopy, default_node_size=node_size)
    to_plot.inherit_edge_colors(False)
    
    if(customizable):
        to_plot.show_buttons(filter_=['physics'])
    else:
        to_plot.set_options(options)
        
    if spatial_position is not None:
        to_plot.toggle_physics(False)

    return (to_plot)
