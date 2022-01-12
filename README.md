# plot_network
A small tool to plot interactive networks.

download locally module in a notebook with:
```
!wget --no-cache --backups=1 https://raw.githubusercontent.com/Yquetzal/plot_network/main/draw_net_interactive.py
```

then import with 
```
from draw_net_interactive import plot_interactive 
```
then call with
plot_interactive(G: nx.Graph, graph_size=800, spatial_position=None, communities=None, labels=True,weight="weight", color=None,
