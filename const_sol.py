# this program reads two csv files, nodes_ok.csv and edges_ok.csv, created by the check_network.py program
# it builds and solves the linear algebraic system of equations to find a constant solution for the network voltages, given some input

import csv
import random as rng
import xlwt
from optparse import OptionParser

#import io

parser = OptionParser()
parser.add_option("-I", "--input", dest="fname",metavar="IM_NAME",
                  help="Choose File name suffix")
parser.add_option("-O", "--output", dest="xls",
                  help="Any value to save xls file")
(optlist, args) = parser.parse_args()

if not optlist.xls:
    xls = False
else:
    xls = True

if not optlist.fname:
    fname = ""
else:
    fname = "_"+optlist.fname

nodes = list(csv.reader(open('data/nodes_ok'+fname+'.csv'), delimiter=","))
edges = list(csv.reader(open('data/edges_ok'+fname+'.csv'), delimiter=","))

ninput = 8
starting = [1,0,1,0]
vinput = []
for i in starting:
    if i == 1:
        vinput.append(-1)
        vinput.append(1)
    else:
        vinput.append(0)
        vinput.append(0)
#vinput = [-1,1,-1,1,-1,1,-1,1]
noutput = 4


pixlen = 20000 / 1024 *0.37 # this is the number of elements in a pixel: if the picture height = width = 20000 nm, a pixel spans 20000/1024 nm
                            # as we suppose that there are 370 elements in 1000 nm we have the above formula
if fname[1:5] == "test":
    pixlen = 1 # for testing
    ninput = 2  # for testing
    noutput = 1
print("number of elements in a pixel: %s" % pixlen)

mynodes = []
myedges = {}
wedges = []
wnodes = []

loading = False
nnodes = 0
# loading structure for nodes: [id, nodes linked, space for coefficients, value of 0 degree term, value of term of the node itself,space to save equation in xls]
for node in nodes:
    if loading == False:
        if node[0] == 'id':
            loading = True
        continue
    mynodes.append([node[0],node[4].split(),[],0,1,""])
    wnodes.append(node[0])
    nnodes = nnodes + 1

print("I consider %s nodes" % nnodes)

loading = False
nedges = 0
# loading structure for edges: 
# 1) dictionary - key (for easy of retrieval): p1-p2, data [p1, p2, lenght in pixels, number of elements, width in pixels, value of first and last element]
# 2) list - [key] (may be useful to index the dictionary)
totlen = 0
timefiber = 0
timehd = 0
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
    w_edge = 0
    try:
        w_edge = float(edge[4])
    except:
        print("Widht error for edge %s" % edge[0])
        pass
    myedges[key] = [int(edge[1]),int(edge[2]),l_edge,round(l_edge*pixlen),w_edge,0,0]
    totlen = totlen + round(l_edge*pixlen)
    timefiber = timefiber + round(l_edge*pixlen)*(96*10**-18)*(6.11*10**6)
#    timehd = timehd + round(l_edge*pixlen)
    wedges.append(key)
    nedges = nedges + 1

print("I consider %s edges" % nedges)
print("Total number of elements: %s" % totlen)
print("Characteristic time with single fiber parameters: %s" % timefiber)
## TODO compute the time to travel the network, as R1C0 (time to discharge an electric unit), using the data for a filament, a hd and a ld bundle and its computed width

# choose random input and output positions; positions are by convention = number of elements from the lower index node
inp_pos = []
inp_edg = []
inp_kedg = []
i=0
while len(inp_edg) < ninput:
    edg = rng.randint(0,nedges-1)
    if edg in inp_edg:
    # don't want 2 input positions in the same edge!
        continue
    inp_edg.append(edg)
    tmp = myedges[wedges[edg]]
    inp_kedg.append(wedges[edg])
    pos = rng.randint(0,tmp[3]-1)
    inp_pos.append(pos)
    print("input %s in edge %s at pos %s" % (i,wedges[edg],pos))
    i = i + 1
#print(inp_edg)
#print(inp_pos)

if fname == "_test":
# for testing:
# test data:
    inp_edg = [0,2]
    inp_kedg= ["1-3","4-2"]
    inp_pos = [0,2]
# test1 data:
if fname == "_test1":
    inp_edg = [0,7]
    inp_kedg= ["2-1","4-2"]
    inp_pos = [0,1]
# end testing values

out_pos = []
out_edg = []
i=0
while len(out_edg) < noutput:
    edg = rng.randint(0,nedges-1)
    if edg in out_edg:
    # don't want 2 output positions in the same edge!
        print(edg)
        print(out_edg)
        continue
    if edg in inp_edg:
    # don't want output and input positions in the same edge!
        continue
    out_edg.append(edg)
    tmp = myedges[wedges[edg]]
    pos = rng.randint(0,tmp[3]-1)
    out_pos.append(pos)
    print("output %s in edge %s at pos %s" % (i,wedges[edg],pos))
    i = i + 1
#print(out_edg)
#print(out_pos)

# prepare the equations for nodes
for node in mynodes:
    n = len(node[1])
    m = wnodes.index(node[0])+2
#    if n == 1:
#    # do not consider outer nodes???
#        continue
    equat = "=-%s*C%s" % (n,m)
    for linked in node[1]:
        key = node[0]+'-'+linked
        if key in myedges:
            edge = myedges[key]
        else:
            key = linked+'-'+node[0]
            if key in myedges:
                edge = myedges[key]
            else:
                print("Edge between node %s and %s not found" % (node[0],linked))
                raise("v")
        #print("L edge %s-%s = %s" % (edge[0], edge[1], edge[3]))

##################################
#        if (edge[0] == 0 and edge[1]==int(node[0])) or (edge[1] == 0 and edge[0]==int(node[0])):
#        # the linked node is an outer one, we consider only the node we are dealing with, and remove the linked external node from the list
#            node[4] = node[4] - 1/(edge[3])*(1/n)     # was (1/(n+1)) and edge[3]+1
#            pp = node[1].index(linked)
#            #node[1].pop(pp)
#            node[1][pp] = "x" # to remove
#            equat = equat + "+%s*C%s" % (1/(1+edge[3]),m)
#            print("linked to outer")
#        elif (edge[0] == 0 and edge[1]!=int(node[0])) or (edge[1] == 0 and edge[0]!=int(node[0])):
#        # we are dealing with an outer node, we add the coefficient of the other and leave its own coeff = 1
#            node[2].append((edge[3]-1)/(edge[3])*(1/n)) #    # was (1/(n+1)) coefficient goes in the same position as the node in the other tuple
#            equat = equat + "+%s*C%s" % ((edge[3]-1)/(edge[3]),wnodes.index(linked)+2)
#            print("outer node")
#        else:
##            node[4] = node[4] - 1/(1+edge[3])*(1/n)   # was (1/(n+1))
##            node[2].append(edge[3]/(1+edge[3])*(1/n)) #    # was (1/(n+1)) coefficient goes in the same position as the node in the other tuple
#            node[4] = node[4] - 1/(edge[3])*(1/n)   # was (1/(n+1))
#            node[2].append((edge[3]-1)/(edge[3])*(1/n)) #    # was (1/(n+1)) coefficient goes in the same position as the node in the other tuple
#            equat = equat + "+%s*C%s" % (1/(edge[3]),m)
#            equat = equat + "+%s*C%s" % ((edge[3]-1)/(edge[3]),wnodes.index(linked)+2)
###################################
# da sistemare!
#        node[4] = node[4] - 1/(edge[3])*(1/n)   # was (1/(n+1))
#        node[2].append((edge[3]-1)/(edge[3])*(1/n)) #    # was (1/(n+1)) coefficient goes in the same position as the node in the other tuple
#        equat = equat + "+%s*C%s" % (1/(edge[3]),m)
#        equat = equat + "+%s*C%s" % ((edge[3]-1)/(edge[3]),wnodes.index(linked)+2)
        node[4] = node[4] - (edge[3]-1)/(edge[3])*(1/n)   # was (1/(n+1))
        node[2].append(1/(edge[3])*(1/n)) #    # was (1/(n+1)) coefficient goes in the same position as the node in the other tuple
        equat = equat + "+%s*C%s" % ((edge[3]-1)/(edge[3]),m)
        equat = equat + "+%s*C%s" % (1/(edge[3]),wnodes.index(linked)+2)

# da sistemare!

        # look for 0 degree term
        if key in inp_kedg:
            kk = inp_kedg.index(key)
            pp = inp_pos[kk]
            vv = vinput[kk]
            if vv>0:
                signvv = '-'
            else:
                signvv = '+'
            if node[0] < linked:
                node[3] = node[3] - vv * ((edge[3]-pp)/edge[3])*(1/n)    
                equat = equat + signvv + "%s" % str(abs(vv) * (edge[3]-pp)/edge[3])
            else:
                node[3] = node[3] - vv * (pp/edge[3])*(1/n)    
                equat = equat + signvv + "%s" % str(abs(vv) * pp/edge[3])
            #print(equat)
    # remove marked links
#    while "x" in node[1]:
#        pp=node[1].index("x")
#        node[1].pop(pp)
    # reset to 1 coefficient of node i itself
    #print("node %s coefficients = %s, 0 deg term = %s, its coeff %s" % (node[0], node[2], node[3], node[4]))
    ci = node[4]
    node[4] = 1
    for ii in range(len(node[2])):
        node[2][ii] = node[2][ii]/ci
    node[3] = node[3]/ci
    node[5] = equat

# solve the equations for nodes

print("I start solving the equations")
go_on = True
back = False
while go_on == True:
    if back:
        start1 = len(mynodes) - 1
        stop1 = -1
        step1 = -1
    else:
        start1 = 0
        stop1 = len(mynodes)
        step1 = 1
    for i in range(start1,stop1,step1):
        node = mynodes[i]
        if back:
            start2 = i-1
            stop2 = -1
            step2 = -1
        else:
            start2 = i+1
            stop2 = len(mynodes)
            step2 = 1
        for k in range(start2,stop2,step2):
            nodel = mynodes[k]
            if node[0] not in nodel[1]:
                continue
            pp = nodel[1].index(node[0])
            #print("%s %s %s %s" % (nodel[0], nodel[1], node[0], nodel[2]))
            ci = nodel[2][pp]  # coefficient of node i in the equation of node k
            nodel[1].pop(pp) # clear node i in nodes linked and coefficient lists as it is being replaced by its equation
            nodel[2].pop(pp)
            ill = 0
            for ll in node[1]:
            # add nodes linked to node i, or update their coefficient if already in node k equation
                if ll == nodel[0]:
                # node i depends on node k
                    nodel[4] = nodel[4] - ci*node[2][ill]
                    ill = ill + 1
                    continue
                if not ll in nodel[1]:
                    nodel[1].append(ll)
                    nodel[2].append(ci*node[2][ill])
                else:
                    llp = nodel[1].index(ll)
                    nodel[2][llp] = nodel[2][llp] + ci*node[2][ill]
                ill = ill + 1
            # manage 0 degree term
            nodel[3] = nodel[3] + ci * node[3]
            # reset to 1 coefficient of node k so it is ready to go into equations for higher indexes
            ci = nodel[4]
            nodel[4] = 1
            for ii in range(len(nodel[2])):
                nodel[2][ii] = nodel[2][ii]/ci
            nodel[3] = nodel[3]/ci
    go_on = False
    still_to_do = 0
    for node in mynodes:
        #print(node[1])
        if node[1]:
            go_on = True
            still_to_do = still_to_do + 1
    print("Still to do: %s" % still_to_do)
    if back == False:
        back = True
    else:
        back = False
##    go_on = False

# print all the nodes' values and equations in xls
if xls == True:
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('Nodes')
    worksheet.write(0,0,"Index")
    worksheet.write(0,1,"Linked to")
    worksheet.write(0,2,"Value")
    worksheet.write(0,3,"Equation")
    i = 1

    for node in mynodes:
        worksheet.write(i,0,node[0])
        worksheet.write(i,1,node[1])
        worksheet.write(i,2,node[3])
        tmp = node[5]
        tmp = tmp.replace(".",",")  # for italian excel
        worksheet.write(i,3,tmp)
        i=i+1
#    print("Node %s: %s (check: 1=%s)" % (node[0],round(node[3],3),node[4]))

    workbook.save('data/results'+fname+'.xls')

# compute difference of values in the output points +1 and -1, and divide by the local rsistance to get the current intensities
# we start considering ddp between the nodes of the output edges
i=0
results = []
for edg in out_edg:
    tmp = myedges[wedges[edg]]
    out1=float(mynodes[wnodes.index(str(tmp[0]))][3])
    out2=float(mynodes[wnodes.index(str(tmp[1]))][3])
    print("Potential at the nodes of output %s (%s):" % (i, wedges[edg]))
    print("   Node %s: %s" % (tmp[0], out1))
    print("   Node %s: %s" % (tmp[1], out2))
    diff = out1-out2
    print("   Diff. = %s" % diff)
    if abs(diff)> 1:
        results.append(1)
    else:
        results.append(0)
    i=i+1

print(starting)
print(results)