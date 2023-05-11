#kuang@DEVP ~/MyPrograms/GraphSAGE
#$ cat ./delaunay.py
#!/home/kuang/.conda/envs/py39/bin/python
from libpysal import weights
from libpysal.cg import voronoi_frames
from contextily import add_basemap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import geopandas as gpd
root='/nas2/cmaqruns/2022fcst/fusion/Voronoi/'
boundary=gpd.read_file(root+'boundary_shape.shp')
df2 = gpd.read_file(root+'stn.shp')
boundary_shape = boundary.geometry[0]

df2=df2.reset_index(drop=True)
for i in range(len(df2)):
    p=df2.loc[i,'geometry']
    if not p.within(boundary_shape): # or boundary_shape.exterior.distance(p) < 0.01:
        df2=df2.drop(i)
df2=df2.reset_index(drop=True)
coordinates = np.column_stack((df2.geometry.x, df2.geometry.y))
cells, generators = voronoi_frames(coordinates, clip="convex hull")
delaunay = weights.Rook.from_dataframe(cells)
delaunay_graph = delaunay.to_networkx()
positions = dict(zip(delaunay_graph.nodes, coordinates))
ax = cells.plot(facecolor="lightblue", alpha=0.50, edgecolor="cornsilk", linewidth=2,figsize=(12, 10))
add_basemap(ax)
ax.axis("off")
boundary.plot(ax=ax, color="gray", alpha=0.50)
nx.draw(
    delaunay_graph,
    positions,
    ax=ax,
    node_size=2,
    node_color="k",
    edge_color="k",
    alpha=0.8,
)
ax.set_title('Voronoi and Delaunay links of Taiwan Air Quality Station Networks')
plt.show()
