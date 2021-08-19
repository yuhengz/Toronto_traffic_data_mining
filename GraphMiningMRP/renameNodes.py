import numpy as np
import pandas as pd


def buildTable(nodes):
	keys = nodes['osmid']
	values = nodes.index
	d = dict(zip(keys, values))
	nodes['osmid'] = nodes.index
	return d

def renameEdges(table, edges):
	# for index, row in edges.iterrows():
		# print(row['from'])
		# row['from'] = table[row['from']]
		# row['to'] = table[row['to']]
		# print(row['from'])
		# exit(0)
	for index in edges.index:
		edges.loc[index, 'from'] = table[edges.loc[index, 'from']]
		edges.loc[index, 'to'] = table[edges.loc[index, 'to']]
	# return edges

def main(nodeFile, edgeFile):
	nodes = pd.read_csv(nodeFile)
	edges = pd.read_csv(edgeFile)
	print(nodes.head())
	print(edges.head())
	nodes = nodes.sort_values(by=['osmid'])
	table = buildTable(nodes)
	renameEdges(table, edges)
	print("--------------------")
	print(nodes.head())
	print(edges.head())
	nodes.to_csv('new_nodes.csv', header = True)
	edges.to_csv('new_edges.csv', header=True)






if __name__ == '__main__':
	main("nodes.csv", "edges.csv")