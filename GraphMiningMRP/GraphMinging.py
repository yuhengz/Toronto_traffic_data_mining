#!/usr/bin/env python
# coding: utf-8

# In[2]:


# pip install cairocffi


# In[2]:


# pip install python-igraph


# In[1]:


import folium as flm 
import igraph as ig
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

g_edges = pd.read_csv('new_edges.csv')


# In[7]:


a = g_edges['from']
list_from = [str(x) for x in a]

b = g_edges['to']

list_to = [str(x) for x in b]

g_node = pd.read_csv('new_nodes.csv')

# print(type(g_node['osmid'][0]))

g_node['osmid'] = g_node['osmid'].astype('str')
nv = len(g_node.index)

# print(type(g_node['osmid'][0]))
# exit(0)

# g_node['id']

c = g_node['osmid']

# c

list_node = [str(x) for x in c]


# In[8]:

print("{:-^60}".format(" adding edges to igraph.Graph "))

g = ig.Graph(directed=True)
g.add_vertices(nv)
for i in tqdm(range(len(list_from))):
    g.add_edge(a[i], b[i])


# In[9]:


g.es['weight'] = g_edges['length']
g.es['speed'] = g_edges['maxspeed']

g.vs['longitude'] = list(g_node['x'])
g.vs['latitude'] = list(g_node['y'])
g.vs['layout'] = [(v['longitude'],v['latitude']) for v in g.vs]

g.vs['color'] = "black"


# In[10]:


pd.Series(g.indegree()).value_counts(normalize=True, sort=False)

pd.Series(g.outdegree()).value_counts(normalize=True, sort=False)

ly = ig.Layout(g.vs['layout'])
ly.mirror(1)


# In[17]:


pl1 = ig.plot(g, layout=ly, vertex_size=3, edge_arrow_size=0.01, edge_arrow_width=0.01, edge_curved=0)
pl1.save("pl1.png")
print("{:-^60}".format(" pl1 is saved"))


# In[18]:


MAP_BOUNDS = ((43.8492658-0.0000001, -79.3112439-0.0000001), (43.8535154+0.0000001, -79.3380466+0.0000001))
m_plot = flm.Map()

for v in g.vs:
    flm.Circle(
        (v['latitude'], v['longitude']),
        radius=1, weight=1,
        color=v['color'], fill=True, fill_color=v['color']).add_to(m_plot)

for e in g.es:
    v1 = g.vs[e.source]
    v2 = g.vs[e.target]
    flm.PolyLine(
        [(v1['latitude'], v1['longitude']), (v2['latitude'], v2['longitude'])],
        color="black", weight=1).add_to(m_plot)

flm.Rectangle(MAP_BOUNDS, color="blue",weight=4).add_to(m_plot)
m_plot.fit_bounds(MAP_BOUNDS)
# m_plot.save("map1.html")
# print("{:-^60}".format(" map1 is saved"))


# In[21]:


bet = g.betweenness()
plt.hist(bet, 50);


# In[22]:


very_heavy_usage = np.quantile(bet, 0.99)
heavy_usage = np.quantile(bet, 0.9)

g.vs['size'] = [1 if b < heavy_usage else 7 if b < very_heavy_usage else 14 for b in bet]


# In[23]:


ly = ig.Layout(g.vs['layout'])
ly.mirror(1)
pl2 = ig.plot(g, layout=ly, vertex_size=g.vs['size'], vertex_color=g.vs['color'], edge_arrow_size=0.01, edge_arrow_width=0.01, edge_curved=0)
pl2.save("pl2.png")
print("{:-^60}".format(" pl2 is saved"))


# In[25]:


MAP_BOUNDS = ((43.8492658-0.0000001, -79.3112439-0.0000001), (43.8535154+0.0000001, -79.3380466+0.0000001))
m_plot = flm.Map()

for v in g.vs:
    flm.Circle(
        (v['latitude'], v['longitude']),
        radius=1, color=v['color'], weight= v['size'],
        fill=True, fill_color=v['color']).add_to(m_plot)

for e in g.es:
    v1 = g.vs[e.source]
    v2 = g.vs[e.target]
    flm.PolyLine(
        [(v1['latitude'], v1['longitude']), (v2['latitude'], v2['longitude'])],
        color="red", weight=1).add_to(m_plot)

flm.Rectangle(MAP_BOUNDS, color="blue",weight=4).add_to(m_plot)
m_plot.fit_bounds(MAP_BOUNDS)
# m_plot.save("map2.html")
# print("{:-^60}".format(" map2 is saved"))

bet = g.betweenness()
plt.hist(bet, 50);

very_heavy_usage = np.quantile(bet, 0.99)
heavy_usage = np.quantile(bet, 0.9)

g.vs['size'] = [1 if b < heavy_usage else 7 if b < very_heavy_usage else 14 for b in bet]

ly = ig.Layout(g.vs['layout'])
ly.mirror(1)
pl3 = ig.plot(g, layout=ly, vertex_size=g.vs['size'], vertex_color=g.vs['color'], edge_arrow_size=0.01, edge_arrow_width=0.01, edge_curved=0)
pl3.save("pl3.png")
print("{:-^60}".format(" pl3 is saved"))

MAP_BOUNDS = ((43.8492658-0.0000001, -79.3112439-0.0000001), (43.8535154+0.0000001, -79.3380466+0.0000001))
m_plot = flm.Map()

for v in g.vs:
    flm.Circle(
        (v['latitude'], v['longitude']),
        radius=1, color=v['color'], weight= v['size'],
        fill=True, fill_color=v['color']).add_to(m_plot)

for e in g.es:
    v1 = g.vs[e.source]
    v2 = g.vs[e.target]
    flm.PolyLine(
        [(v1['latitude'], v1['longitude']), (v2['latitude'], v2['longitude'])],
        color="red", weight=1).add_to(m_plot)

flm.Rectangle(MAP_BOUNDS, color="blue",weight=4).add_to(m_plot)
m_plot.fit_bounds(MAP_BOUNDS)
m_plot.save("map3.html")
print("{:-^60}".format(" map3 is saved"))

bet = g.betweenness(weights=g.es['weight'])
plt.hist(bet, 50)

very_heavy_usage = np.quantile(bet, 0.99)
heavy_usage = np.quantile(bet, 0.9)

g.vs['size'] = [1 if b < heavy_usage else 7 if b < very_heavy_usage else 14 for b in bet]

ly = ig.Layout(g.vs['layout'])
ly.mirror(1)
pl4 = ig.plot(g, layout=ly, vertex_size=g.vs['size'], vertex_color=g.vs['color'], edge_arrow_size=0.01, edge_arrow_width=0.01, edge_curved=0)
pl4.save("pl4.png")
print("{:-^60}".format(" pl4 is saved"))

MAP_BOUNDS = ((43.8492658-0.0000001, -79.3112439-0.0000001), (43.8535154+0.0000001, -79.3380466+0.0000001))
m_plot = flm.Map()
for v in g.vs:
    flm.Circle(
        (v['latitude'], v['longitude']),
        radius=1, color=v['color'], weight= v['size'],
        fill=True, fill_color=v['color']).add_to(m_plot)

for e in g.es:
    v1 = g.vs[e.source]
    v2 = g.vs[e.target]
    flm.PolyLine(
        [(v1['latitude'], v1['longitude']), (v2['latitude'], v2['longitude'])],
        color="red", weight=1).add_to(m_plot)

flm.Rectangle(MAP_BOUNDS, color="blue",weight=4).add_to(m_plot)
m_plot.fit_bounds(MAP_BOUNDS)
m_plot.save("map4.html")
print("{:-^60}".format(" map4 is saved"))


bet = g.betweenness(weights=g.es['weight'] / g_edges["maxspeed"])
plt.hist(bet, 50);

very_heavy_usage = np.quantile(bet, 0.99)
heavy_usage = np.quantile(bet, 0.9)

g.vs['size'] = [1 if b < heavy_usage else 7 if b < very_heavy_usage else 14 for b in bet]

ly = ig.Layout(g.vs['layout'])
ly.mirror(1)
pl5 = ig.plot(g, layout=ly, vertex_size=g.vs['size'], vertex_color=g.vs['color'], edge_arrow_size=0.01, edge_arrow_width=0.01, edge_curved=0)
pl5.save("pl5.png")
print("{:-^60}".format(" pl5 is saved"))

MAP_BOUNDS = ((43.8492658-0.0000001, -79.3112439-0.0000001), (43.8535154+0.0000001, -79.3380466+0.0000001))
m_plot = flm.Map()
for v in g.vs:
    flm.Circle(
        (v['latitude'], v['longitude']),
        radius=1, color=v['color'], weight= v['size'],
        fill=True, fill_color=v['color']).add_to(m_plot)

for e in g.es:
    v1 = g.vs[e.source]
    v2 = g.vs[e.target]
    flm.PolyLine(
        [(v1['latitude'], v1['longitude']), (v2['latitude'], v2['longitude'])],
        color="red", weight=1).add_to(m_plot)

flm.Rectangle(MAP_BOUNDS, color="blue",weight=4).add_to(m_plot)
m_plot.fit_bounds(MAP_BOUNDS)
m_plot.save("map5.html")
print("{:-^60}".format(" map5 is saved"))

