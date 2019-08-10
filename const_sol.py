# this program reads two csv files, nodes_ok.csv and edges_ok.csv, created by the check_network.py program
# it builds and solves the linear algebraic system of equations to find a constant solution for the network voltages, given some input

import csv
import random as rng
#import io

nodes = list(csv.reader(open('data/nodes_ok.csv'), delimiter=","))
edges = list(csv.reader(open('data/edges_ok.csv'), delimiter=","))

ninput = 8
noutput = 8

pixlen = 20000 / 1024 *0.37 # this is the number of elements in a pixel: if the picture height = width = 20000 nm, a pixel spans 20000/1024 nm
                            # as we suppose that there are 370 elements in 1000 nm we have the above formula
print("number of elements in a pixel: %s" % pixlen)

mynodes = []
myedges = {}
wedges = []

loading = False
nnodes = 0
# loading structure for nodes: [id, nodes linked, space for equation]
for node in nodes:
    if loading == False:
        if node[0] == 'id':
            loading = True
        continue
    mynodes.append([node[0],node[4],[]])
    nnodes = nnodes + 1

print("I consider %s nodes" % nnodes)

loading = False
nedges = 0
# loading structure for edges: 
# 1) dictionary - key (for easy of retrieval): p1-p2, data [p1, p2, lenght in pixel, number of elements, space for equation]
# 2) list - [key] (may be useful to index the dictionary)
for edge in edges:
    if loading == False:
        if edge[0] == 'id':
            loading = True
        continue
    key = edge[0].strip()
    l_edge = 0
    try:
        l_edge = float(edge[3])
    except:
        print("Lenght error for edge %s" % edge[0])
        pass
    myedges[key] = [edge[0],edge[1],l_edge,round(l_edge*pixlen),[]]
    wedges.append(key)
    nedges = nedges + 1

print("I consider %s edges" % nedges)

inp_pos = []
inp_edg = []
#for i in range(ninput):
i=0
while len(inp_edg) < ninput:
    edg = rng.randint(0,nedges-1)
    if edg in inp_edg:
    # don't want 2 input positions in the same edge!
        continue
    inp_edg.append(edg)
    tmp = myedges[wedges[edg]]
    pos = rng.randint(0,tmp[3])
    inp_pos.append(pos)
    print("input %s in edge %s at pos %s" % (i,wedges[edg],pos))
    i = i + 1
print(inp_edg)
print(inp_pos)

out_pos = []
out_edg = []
i=0
#for i in range(ninput):
while len(out_edg) < noutput:
    edg = rng.randint(0,nedges-1)
    if edg in out_edg:
    # don't want 2 input positions in the same edge!
        continue
    out_edg.append(edg)
    tmp = myedges[wedges[edg]]
    pos = rng.randint(0,tmp[3])
    out_pos.append(pos)
    print("output %s in edge %s at pos %s" % (i,wedges[edg],pos))
    i = i + 1
print(out_edg)
print(out_pos)

