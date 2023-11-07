import networkx as nx
import pandas as pd
from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from includes.df_ops import DataframeOperations

df_ops = DataframeOperations()
user_data = pd.read_csv("output/user_data_081123.csv")
# Read the data from the CSV file
df = df_ops.create_source_target_df(user_data)
attribute_df = df_ops.create_attribute_df(user_data)

G = nx.from_pandas_edgelist(df, "source", "target")

# some bug fix according to stackoverflow
mapping = dict((n, i) for i, n in enumerate(G.nodes))
H = nx.relabel_nodes(G, mapping)

# draw
degrees = dict(nx.degree(H))
nx.set_node_attributes(H, name="degree", values=degrees)
number_to_adjust_by = 5
adjusted_node_size = dict(
    [(node, degree + number_to_adjust_by) for node, degree in nx.degree(H)]
)
nx.set_node_attributes(H, name="adjusted_node_size", values=adjusted_node_size)
size_by_this_attribute = "adjusted_node_size"
color_by_this_attribute = "adjusted_node_size"
# Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
color_palette = Blues8

# Choose a title!
title = "Steam Friends Network"

# Establish which categories will appear when hovering over each node


# fix here
HOVER_TOOLTIPS = [
    ("id", "@id"),
    ("name", "@name"),
    ("country", "@country"),
    ("degree", "@degree"),
]

# Create a plot — set dimensions, toolbar, and title
plot = figure(
    tooltips=HOVER_TOOLTIPS,
    tools="pan,wheel_zoom,save,reset",
    active_scroll="wheel_zoom",
    x_range=Range1d(-10.1, 10.1),
    y_range=Range1d(-10.1, 10.1),
    title=title,
)

# Create a network graph object
network_graph = from_networkx(H, nx.spring_layout, scale=10, center=(0, 0))

# Set node sizes and colors according to node degree (color as spectrum of color palette)
minimum_value_color = min(
    network_graph.node_renderer.data_source.data[color_by_this_attribute]
)
maximum_value_color = max(
    network_graph.node_renderer.data_source.data[color_by_this_attribute]
)
network_graph.node_renderer.glyph = Circle(
    size=size_by_this_attribute,
    fill_color=linear_cmap(
        color_by_this_attribute, color_palette, minimum_value_color, maximum_value_color
    ),
)

# Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

plot.renderers.append(network_graph)

show(plot)
save(plot, filename=f"{title}.html")
