# this program reads two csv files, nodes_ok.csv and edges_ok.csv, created by the check_network.py program
# it builds and solves the linear algebraic system of equations to find a constant solution for the network voltages, given some input

import csv
import random as rng
import xlwt
from optparse import OptionParser
import math

#import io

parser = OptionParser()
parser.add_option("-I", "--input", dest="fname",metavar="IM_NAME",
                  help="Choose File name suffix")
parser.add_option("-O", "--output", dest="xls",
                  help="Any value to save xls file")
parser.add_option("-E", "--edges", dest="rndinp",
                  help="File name of csv with input/output positions, otherwise random positions are used")
(optlist, args) = parser.parse_args()

if not optlist.xls:
    xls = False
else:
    xls = True

if not optlist.fname:
    fname = ""
else:
    fname = "_"+optlist.fname

if not optlist.rndinp:
    rndinp = ""
else:
    rndinp = "_"+optlist.rndinp

nodes = list(csv.reader(open('data/nodes_ok'+fname+'.csv'), delimiter=","))
edges = list(csv.reader(open('data/edges_ok'+fname+'.csv'), delimiter=","))
inits = list(csv.reader(open('data/inits_ok'+fname+'.csv'), delimiter=","))

ninput = 8
noutput = 4


pixlen = 20000 / 1024 *0.37 # this is the number of elements in a pixel: if the picture height = width = 20000 nm, a pixel spans 20000/1024 nm
                            # as we suppose that there are 370 elements in 1000 nm we have the above formula
pixnano = 20 / 1024 * 10**-6
print("number of elements in a pixel: %s" % pixlen)

#########################
# Initial loading of the network and choice of the input and output positions
#########################

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
# 1) dictionary - key (for easy of retrieval): p1-p2, data [p1, p2, lenght in pixels, number of elements, width in pixels, values of extremes with 3 different thresholds]
# 2) list - [key] (may be useful to index the dictionary)
totlen = 0
rhokna = 1/(7.4*0.15+5*0.02)
print("rhokna: %s" % rhokna)
bjerr = 0.000000000712888
pi2l =2*math.pi*5.4*10**-9
print("pi2l: %s" % pi2l)
rhokna = rhokna / pi2l
print("rhokna: %s" % rhokna)
epsi = 80 * 8.854187817*10**-12
filperpix2 = 0.24 # we take the mean of the filaments per bundle reported by experiments (50-60 +-25 = (25+85)/2 = 55 and the area of a circle with the average radius found (8.48) = 226
                  # and consider 55 / 226 the number of fibers in a circle of a pixel radius
timefiber = 0  # values for 0.713 Bjerrum length
timehd = 0
timeld = 0
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
    myedges[key] = [int(edge[1]),int(edge[2]),l_edge,round(l_edge*pixlen),w_edge,[],[],[]]
    totlen = totlen + round(l_edge*pixlen)
    timefiber = timefiber + round(l_edge*pixlen)*(102.6*10**-18)*(5.7*10**6)
    rbun = w_edge * pixnano
    logar = math.log((bjerr+rbun)/rbun)
    c0hd = pi2l * epsi / logar
    r1hd = rhokna * logar
    timehd = timehd + round(l_edge*pixlen)* c0hd * r1hd
    nfibers = round(math.pi * w_edge**2 * filperpix2,0)
    if nfibers > 0:
        timeld = timeld + round(l_edge*pixlen)*(102.6*10**-18/nfibers)*(5.7*10**6/nfibers)
    wedges.append(key)
    nedges = nedges + 1

print("I consider %s edges" % nedges)
print("Total number of elements: %s" % totlen)
print("Characteristic time with single fiber parameters: %s" % timefiber)
print("Characteristic time with hd bundles parameters: %s" % timehd)
print("Characteristic time with ld bundles parameters: %s" % timeld)

# choose random input and output positions; positions are by convention = number of elements from the lower index node
inp_pos = []
inp_edg = []
inp_kedg = []
out_pos = []
out_edg = []
if not rndinp:
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


    i=0
    while len(out_edg) < noutput:
        edg = rng.randint(0,nedges-1)
        if edg in out_edg:
        # don't want 2 output positions in the same edge!
            print(edg)
            print(out_edg)
            continue
        if edg in inp_edg:
        #don't want output and input positions in the same edge!
            continue
        out_edg.append(edg)
        tmp = myedges[wedges[edg]]
        pos = rng.randint(0,tmp[3]-1)
        out_pos.append(pos)
        print("output %s in edge %s at pos %s" % (i,wedges[edg],pos))
        i = i + 1

else:
    positions = list(csv.reader(open('data/posits_ok'+rndinp+'.csv'), delimiter=","))
    inp_kedg.append(positions[0][0])
    inp_pos.append(int(positions[0][1]))
    inp_edg.append(wedges.index(positions[0][0]))
    inp_kedg.append(positions[1][0])
    inp_pos.append(int(positions[1][1]))
    inp_edg.append(wedges.index(positions[1][0]))
    inp_kedg.append(positions[2][0])
    inp_pos.append(int(positions[2][1]))
    inp_edg.append(wedges.index(positions[2][0]))
    inp_kedg.append(positions[3][0])
    inp_pos.append(int(positions[3][1]))
    inp_edg.append(wedges.index(positions[3][0]))
    inp_kedg.append(positions[4][0])
    inp_pos.append(int(positions[4][1]))
    inp_edg.append(wedges.index(positions[4][0]))
    inp_kedg.append(positions[5][0])
    inp_pos.append(int(positions[5][1]))
    inp_edg.append(wedges.index(positions[5][0]))
    inp_kedg.append(positions[6][0])
    inp_pos.append(int(positions[6][1]))
    inp_edg.append(wedges.index(positions[6][0]))
    inp_kedg.append(positions[7][0])
    inp_pos.append(int(positions[7][1]))
    inp_edg.append(wedges.index(positions[7][0]))
    out_pos.append(int(positions[8][1]))
    out_edg.append(wedges.index(positions[8][0]))
    out_pos.append(int(positions[9][1]))
    out_edg.append(wedges.index(positions[9][0]))
    out_pos.append(int(positions[10][1]))
    out_edg.append(wedges.index(positions[10][0]))
    out_pos.append(int(positions[11][1]))
    out_edg.append(wedges.index(positions[11][0]))
    i=0
    for posi in positions:
        if i<8:
            print("input in edge %s at position %s" % (posi[0],posi[1]))
        else:
            print("output in edge %s at position %s" % (posi[0],posi[1]))
        i=i+1

#######################
# start cycling on initial values
#######################
outr = []
outr05 = []
outr2 = []
nturn = 1
for starting in inits:
    vinput = []
    for i in starting:
        if i == '1':
            vinput.append(-1)
            vinput.append(1)
        else:
            vinput.append(0)
            vinput.append(0)

# prepare the equations for nodes

# reload the data of nodes, as they are changed during the processing

    mynodes = []
    loading = False
    # loading structure for nodes: [id, nodes linked, space for coefficients, value of 0 degree term, value of term of the node itself,space to save equation in xls]
    for node in nodes:
        if loading == False:
            if node[0] == 'id':
                loading = True
            continue
        mynodes.append([node[0],node[4].split(),[],0,1,""])

    for node in mynodes:
        n = len(node[1])
        m = wnodes.index(node[0])+2
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
            node[4] = node[4] - (edge[3]-1)/(edge[3])*(1/n)   # was (1/(n+1))
            node[2].append(1/(edge[3])*(1/n)) #    # was (1/(n+1)) coefficient goes in the same position as the node in the other tuple
            equat = equat + "+%s*C%s" % ((edge[3]-1)/(edge[3]),m)
            equat = equat + "+%s*C%s" % (1/(edge[3]),wnodes.index(linked)+2)


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
                # to manage 2 input input in the same edge
                if key in inp_kedg[kk+1:]:
                    jj = inp_kedg[kk+1:].index(key)
                    kk * kk+jj+1
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

        # reset to 1 coefficient of node i itself
        ci = node[4]
        node[4] = 1
        for ii in range(len(node[2])):
            node[2][ii] = node[2][ii]/ci
        node[3] = node[3]/ci
        node[5] = equat

    # solve the equations for nodes

    print("I start solving the equations for input %s" % starting)
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
#            worksheet.write(i,3,xlwt.Formula(tmp))
            worksheet.write(i,3,tmp)
            i=i+1
#    print("Node %s: %s (check: 1=%s)" % (node[0],round(node[3],3),node[4]))

        workbook.save('data/results'+str(nturn)+fname+'.xls')
    nturn = nturn + 1
# compute difference of values in the output points +1 and -1, and divide by the local rsistance to get the current intensities
# we start considering ddp between the nodes of the output edges
    i=0
    results = []
    results05 = []
    results2 = []

    for edg in out_edg:
        tmp = myedges[wedges[edg]]
        out1=float(mynodes[wnodes.index(str(tmp[0]))][3])
        out2=float(mynodes[wnodes.index(str(tmp[1]))][3])
#        print("Potential at the nodes of output %s (%s):" % (i, wedges[edg]))
#        print("   Node %s: %s" % (tmp[0], out1))
#        print("   Node %s: %s" % (tmp[1], out2))
        diff = out1-out2
#        print("   Diff. = %s" % diff)
        if abs(diff)>= 1:
            results.append(1)
        else:
            results.append(0)
        if abs(diff)>= 0.5:
            results05.append(1)
        else:
            results05.append(0)
        if abs(diff)>= 2:
            results2.append(1)
        else:
            results2.append(0)
        i=i+1

    outr.append(results)
    outr05.append(results05)
    outr2.append(results2)
    print(starting)
    print(results)
    print("====================")
#   save all the results to look for logical gates
    for edg in wedges:
        myedg=myedges[edg]
        out1=float(mynodes[wnodes.index(str(myedg[0]))][3])
        out2=float(mynodes[wnodes.index(str(myedg[1]))][3])
        diff = abs(out1-out2)
        if diff>=0.5:
            myedg[5].append(1)
        else:
            myedg[5].append(0)
        if diff>=1:
            myedg[6].append(1)
        else:
            myedg[6].append(0)
        if diff>=2:
            myedg[7].append(1)
        else:
            myedg[7].append(0)

workbookr = xlwt.Workbook(encoding='utf8')
worksheetr = workbookr.add_sheet('Results')
worksheetr.write(0,0,"I1")
worksheetr.write(0,1,"I2")
worksheetr.write(0,2,"I3")
worksheetr.write(0,3,"I4")
worksheetr.write(0,4,"O1-1")
worksheetr.write(0,5,"O2-1")
worksheetr.write(0,6,"O3-1")
worksheetr.write(0,7,"O4-1")
worksheetr.write(0,10,"I1")
worksheetr.write(0,11,"I2")
worksheetr.write(0,12,"I3")
worksheetr.write(0,13,"I4")
worksheetr.write(0,14,"O1-05")
worksheetr.write(0,15,"O2-05")
worksheetr.write(0,16,"O3-05")
worksheetr.write(0,17,"O4-05")
worksheetr.write(0,20,"I1")
worksheetr.write(0,21,"I2")
worksheetr.write(0,22,"I3")
worksheetr.write(0,23,"I4")
worksheetr.write(0,24,"O1-2")
worksheetr.write(0,25,"O2-2")
worksheetr.write(0,26,"O3-2")
worksheetr.write(0,27,"O4-2")

i = 1
k = 0
for starting in inits:
    worksheetr.write(i,0,starting[0])
    worksheetr.write(i,1,starting[1])
    worksheetr.write(i,2,starting[2])
    worksheetr.write(i,3,starting[3])
    worksheetr.write(i,4,outr[k][0])
    worksheetr.write(i,5,outr[k][1])
    worksheetr.write(i,6,outr[k][2])
    worksheetr.write(i,7,outr[k][3])
    worksheetr.write(i,10,starting[0])
    worksheetr.write(i,11,starting[1])
    worksheetr.write(i,12,starting[2])
    worksheetr.write(i,13,starting[3])
    worksheetr.write(i,14,outr05[k][0])
    worksheetr.write(i,15,outr05[k][1])
    worksheetr.write(i,16,outr05[k][2])
    worksheetr.write(i,17,outr05[k][3])
    worksheetr.write(i,20,starting[0])
    worksheetr.write(i,21,starting[1])
    worksheetr.write(i,22,starting[2])
    worksheetr.write(i,23,starting[3])
    worksheetr.write(i,24,outr2[k][0])
    worksheetr.write(i,25,outr2[k][1])
    worksheetr.write(i,26,outr2[k][2])
    worksheetr.write(i,27,outr2[k][3])
    i=i+1
    k=k+1
#    print("Node %s: %s (check: 1=%s)" % (node[0],round(node[3],3),node[4]))

print("Saving results")

workbookr.save('data/poss_gates'+fname+'.xls')

workbookt = xlwt.Workbook(encoding='utf8')
worksheett = workbookt.add_sheet('Results')

worksheett.write(0,0,"Input positions")
i=1
worksheett.write(i,0,"Edge")
worksheett.write(i,1,"Position")
k=0
for edg in inp_kedg:
    i=i+1
    worksheett.write(i,0,edg)
    worksheett.write(i,1,inp_pos[k])
    k=k+1
i=i+2
k=1
worksheett.write(i,0,"Configurations")
i=i+1
worksheett.write(i,0,"Conf. Num.")
worksheett.write(i,1,"I1")
worksheett.write(i,2,"I2")
worksheett.write(i,3,"I3")
worksheett.write(i,4,"I4")

for starting in inits:
    i=i+1
    worksheett.write(i,0,k)
    worksheett.write(i,1,starting[0])
    worksheett.write(i,2,starting[1])
    worksheett.write(i,3,starting[2])
    worksheett.write(i,4,starting[3])
    k=k+1
i=i+2
worksheett.write(i,0,"Results")
i=i+1
worksheett.write(i,0,"Edge")
worksheett.write(i,1,"Threshold = 0.5")
worksheett.write(i,17,"Threshold = 1.0")
worksheett.write(i,33,"Threshold = 2.0")

for edg in wedges:
    i=i+1
    myedg=myedges[edg]
    worksheett.write(i,0,edg)
    k=1
    for diff in myedg[5]:
        worksheett.write(i,k,diff)
        k=k+1
    for diff in myedg[6]:
        worksheett.write(i,k,diff)
        k=k+1
    for diff in myedg[7]:
        worksheett.write(i,k,diff)
        k=k+1


workbookt.save('data/all_poss_gates'+fname+'.xls')
