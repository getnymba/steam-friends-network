import networkx as nx
import pandas as pd
from bokeh.io import show, save
from bokeh.models import Range1d, Circle, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8
from bokeh.transform import linear_cmap
from includes.data_scrape import Scraper
from includes.df_ops import DataframeOperations
import asyncio
from data_collect import Finder

input = input("Enter steam profile link: ")


async def get_data():
    finder = Finder(Scraper(), DataframeOperations())
    await finder.find_st4ck(input)


asyncio.run(get_data())

df_ops = DataframeOperations()
user_data = pd.read_csv("./output/data.csv")

# Read the data from the CSV file
df = df_ops.create_source_target_df(user_data)
G = nx.Graph()
G.add_nodes_from(user_data["id"].tolist())
G.add_edges_from(list(df.to_records(index=False)))
# some bug fix according to stackoverflow
mapping = dict((n, i) for i, n in enumerate(G.nodes))
H = nx.relabel_nodes(G, mapping)

# St4ck's key
st4ck_key = mapping["St4ck"]

# Degree
degrees = dict(nx.degree(H))
nx.set_node_attributes(H, name="degree", values=degrees)

# Adjust node size
number_to_adjust_by = 5
adjusted_node_size = dict(
    [(node, degree + number_to_adjust_by) for node, degree in nx.degree(H)]
)
# Adjust the size of St4ck's node & one's node
adjusted_node_size[0] += 15
adjusted_node_size[st4ck_key] += 15

nx.set_node_attributes(H, name="adjusted_node_size", values=adjusted_node_size)
size_by_this_attribute = "adjusted_node_size"
color_by_this_attribute = "adjusted_node_size"
color_palette = Blues8

# id
id = dict((i, n) for i, n in enumerate(mapping))
nx.set_node_attributes(H, name="id", values=id)
title = "How far are you from St4ck?"

# Tooltip
HOVER_TOOLTIPS = [
    ("id", "@id"),
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
