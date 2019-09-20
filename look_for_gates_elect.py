# this program reads all_possgates_xxx.csv extracted from the output of cycl_const_sol.py, all_gates_xxx.xls. (xxx is the name given to the program run)
# the csv must contain the edge name "node-node" and the results of computation for 4 input 4 output electrodes
# with results for all the 4 input 1/0 possible configurations as contained in file inits_ok_true.csv (this file must not be changed)
# results are 16 columns containing 0 if the value for the configuration is lower than the 0.5 threshold, 1 otherwise,
# 16 columns with 1 as threshold value and 16 with 2 as threshold value
# the program checks for every edge if 2 of the possible input combinations and 1 of the output values give a NOT port, and
# if 4 of the possible input combinations and 1 of the output values give an AND, OR or XOR port, and save the corresponding edge, 
# states, etc. in a new xls file found_gates_xxx.xls
# the program saves the case with the highest threshold

import csv
import xlwt
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-I", "--input", dest="fname",metavar="IM_NAME",
                  help="Choose File name suffix")
parser.add_option("-S", "--nstates", dest="nstates",
                  help="Any value to compute 6 states, otherwise 4 states are computed")
(optlist, args) = parser.parse_args()

if not optlist.fname:
    fname = ""
else:
    fname = "_"+optlist.fname

check_not = []
check_others = []
if not optlist.nstates:
    nstates = 4
    inits = list(csv.reader(open('data/inits_ok4.csv'), delimiter=","))
    check_not.append([4,[(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13),(14,15)]])
    check_not.append([3,[(1,3),(2,0),(7,5),(6,4),(11,9),(10,8),(15,13),(14,12)]])
    check_not.append([2,[(1,5),(0,4),(3,7),(2,6),(9,13),(8,12),(11,15),(10,14)]])
    check_not.append([1,[(1,9),(0,8),(3,11),(2,10),(5,13),(4,12),(7,15),(6,14)]])
    check_others.append([(1,2),[(14,6,10,2),(15,7,11,3),(12,4,8,0),(13,5,9,1)],"1-2"])
    check_others.append([(1,3),[(14,6,12,4),(15,7,13,5),(10,2,8,0),(11,3,9,1)],"1-3"])
    check_others.append([(1,4),[(14,15,6,7),(12,13,4,5),(10,11,2,3),(8,9,0,1)],"1-4"])
    check_others.append([(2,3),[(10,14,8,12),(11,15,9,13),(2,6,0,4),(3,7,1,5)],"2-3"])
    check_others.append([(2,4),[(10,11,14,15),(8,9,12,13),(2,3,6,7),(0,1,4,5)],"2-4"])
    check_others.append([(3,4),[(0,1,2,3),(4,5,6,7),(8,9,10,11),(12,13,14,15)],"3-4"])
else:
    nstates = 6
    # this case will be managed by a dedicated program

edges = list(csv.reader(open('data/all_possgates'+fname+'.csv'), delimiter=","))

for ini in inits:
    tmp=""
    i = 0
    for ini1 in ini:
        tmp=tmp+ini1
        ini[i] = int(ini1)
        i=i+1
    ini.append(tmp)



# tables for found gates, each element is a list containing: the edge, the threshold, the input bit(s), a list of (input state, result)
found_not = []
found_and = []
found_or = []
found_xor = []
nand2 = 0
nand1 = 0
nand05 = 0
nnot2 = 0
nnot1 = 0
nnot05 = 0
nor2 = 0
nor1 = 0
nor05 = 0
nxor2 = 0
nxor1 = 0
nxor05 = 0

k=0
for edg in edges:
    for tocheck in check_not:
        bc = tocheck[0]-1
        for elem in tocheck[1]:
            if inits[elem[0]][bc] != int(edg[elem[0]+33]) and inits[elem[1]][bc] != int(edg[elem[1]+33]):
                found_not.append([edg[0],2.0,bc+1,[(inits[elem[0]][4],edg[elem[0]+33]),(inits[elem[1]][4],edg[elem[1]+33])]])
                nnot2 = nnot2 + 1
                #continue
            if inits[elem[0]][bc] != int(edg[elem[0]+17]) and inits[elem[1]][bc] != int(edg[elem[1]+17]):
                found_not.append([edg[0],1.0,bc+1,[(inits[elem[0]][4],edg[elem[0]+17]),(inits[elem[1]][4],edg[elem[1]+17])]])
                nnot1 = nnot1 + 1
                #continue
            if inits[elem[0]][bc] != int(edg[elem[0]+1]) and inits[elem[1]][bc] != int(edg[elem[1]+1]):
                found_not.append([edg[0],0.5,bc+1,[(inits[elem[0]][4],edg[elem[0]+1]),(inits[elem[1]][4],edg[elem[1]+1])]])
                nnot05 = nnot05 + 1

    for tocheck in check_others:
        bc1 = tocheck[0][0]-1
        bc2 = tocheck[0][1]-1
        for elem in tocheck[1]:
        # OR
            if (inits[elem[0]][bc1] or inits[elem[0]][bc2]) == int(edg[elem[0]+33]) and (inits[elem[1]][bc1] or inits[elem[1]][bc2]) == int(edg[elem[1]+33]) and \
                (inits[elem[2]][bc1] or inits[elem[2]][bc2]) == int(edg[elem[2]+33]) and (inits[elem[3]][bc1] or inits[elem[3]][bc2]) == int(edg[elem[3]+33]):
                found_or.append([edg[0],2.0,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+33]),(inits[elem[1]][4],edg[elem[1]+33]),(inits[elem[2]][4],edg[elem[2]+33]),(inits[elem[3]][4],edg[elem[3]+33])]])
                nor2 = nor2 + 1
            if (inits[elem[0]][bc1] or inits[elem[0]][bc2]) == int(edg[elem[0]+17]) and (inits[elem[1]][bc1] or inits[elem[1]][bc2]) == int(edg[elem[1]+17]) and \
                (inits[elem[2]][bc1] or inits[elem[2]][bc2]) == int(edg[elem[2]+17]) and (inits[elem[3]][bc1] or inits[elem[3]][bc2]) == int(edg[elem[3]+17]):
                found_or.append([edg[0],1.0,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+17]),(inits[elem[1]][4],edg[elem[1]+17]),(inits[elem[2]][4],edg[elem[2]+17]),(inits[elem[3]][4],edg[elem[3]+17])]])
                nor1 = nor1 + 1
            if (inits[elem[0]][bc1] or inits[elem[0]][bc2]) == int(edg[elem[0]+1]) and  (inits[elem[1]][bc1] or inits[elem[1]][bc2]) == int(edg[elem[1]+1]) and \
                (inits[elem[2]][bc1] or inits[elem[2]][bc2]) == int(edg[elem[2]+1]) and (inits[elem[3]][bc1] or inits[elem[3]][bc2]) == int(edg[elem[3]+1]):
                found_or.append([edg[0],0.5,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+1]),(inits[elem[1]][4],edg[elem[1]+1]),(inits[elem[2]][4],edg[elem[2]+1]),(inits[elem[3]][4],edg[elem[3]+1])]])
                nor05 = nor05 + 1
        # AND
            if (inits[elem[0]][bc1] and inits[elem[0]][bc2]) == int(edg[elem[0]+33]) and (inits[elem[1]][bc1] and inits[elem[1]][bc2]) == int(edg[elem[1]+33]) and \
                (inits[elem[2]][bc1] and inits[elem[2]][bc2]) == int(edg[elem[2]+33]) and (inits[elem[3]][bc1] and inits[elem[3]][bc2]) == int(edg[elem[3]+33]):
                found_and.append([edg[0],2.0,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+33]),(inits[elem[1]][4],edg[elem[1]+33]),(inits[elem[2]][4],edg[elem[2]+33]),(inits[elem[3]][4],edg[elem[3]+33])]])
                nand2 = nand2 + 1
            if (inits[elem[0]][bc1] and inits[elem[0]][bc2]) == int(edg[elem[0]+17]) and (inits[elem[1]][bc1] and inits[elem[1]][bc2]) == int(edg[elem[1]+17]) and \
                (inits[elem[2]][bc1] and inits[elem[2]][bc2]) == int(edg[elem[2]+17]) and (inits[elem[3]][bc1] and inits[elem[3]][bc2]) == int(edg[elem[3]+17]):
                found_and.append([edg[0],1.0,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+17]),(inits[elem[1]][4],edg[elem[1]+17]),(inits[elem[2]][4],edg[elem[2]+17]),(inits[elem[3]][4],edg[elem[3]+17])]])
                nand1 = nand1 + 1
            if (inits[elem[0]][bc1] and inits[elem[0]][bc2]) == int(edg[elem[0]+1]) and (inits[elem[1]][bc1] and inits[elem[1]][bc2]) == int(edg[elem[1]+1]) and \
                (inits[elem[2]][bc1] and inits[elem[2]][bc2]) == int(edg[elem[2]+1]) and (inits[elem[3]][bc1] and inits[elem[3]][bc2]) == int(edg[elem[3]+1]):
                found_and.append([edg[0],0.5,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+1]),(inits[elem[1]][4],edg[elem[1]+1]),(inits[elem[2]][4],edg[elem[2]+1]),(inits[elem[3]][4],edg[elem[3]+1])]])
                nand05 = nand05 + 1
        # XOR
            if ((inits[elem[0]][bc1] + inits[elem[0]][bc2])%2) == int(edg[elem[0]+33]) and ((inits[elem[1]][bc1] + inits[elem[1]][bc2])%2) == int(edg[elem[1]+33]) and \
                ((inits[elem[2]][bc1] + inits[elem[2]][bc2])%2) == int(edg[elem[2]+33]) and ((inits[elem[3]][bc1] + inits[elem[3]][bc2])%2) == int(edg[elem[3]+33]):
                found_xor.append([edg[0],2.0,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+33]),(inits[elem[1]][4],edg[elem[1]+33]),(inits[elem[2]][4],edg[elem[2]+33]),(inits[elem[3]][4],edg[elem[3]+33])]])
                nxor2 = nxor2 + 1
            if ((inits[elem[0]][bc1] + inits[elem[0]][bc2])%2) == int(edg[elem[0]+17]) and ((inits[elem[1]][bc1] + inits[elem[1]][bc2])%2) == int(edg[elem[1]+17]) and \
                ((inits[elem[2]][bc1] + inits[elem[2]][bc2])%2) == int(edg[elem[2]+17]) and ((inits[elem[3]][bc1] + inits[elem[3]][bc2])%2) == int(edg[elem[3]+17]):
                found_xor.append([edg[0],1.0,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+17]),(inits[elem[1]][4],edg[elem[1]+17]),(inits[elem[2]][4],edg[elem[2]+17]),(inits[elem[3]][4],edg[elem[3]+17])]])
                nxor1 = nxor1 + 1
            if ((inits[elem[0]][bc1] + inits[elem[0]][bc2])%2) == int(edg[elem[0]+1]) and ((inits[elem[1]][bc1] + inits[elem[1]][bc2])%2) == int(edg[elem[1]+1]) and \
                ((inits[elem[2]][bc1] + inits[elem[2]][bc2])%2) == int(edg[elem[2]+1]) and ((inits[elem[3]][bc1] + inits[elem[3]][bc2])%2) == int(edg[elem[3]+1]):
                found_xor.append([edg[0],0.5,tocheck[2],[(inits[elem[0]][4],edg[elem[0]+1]),(inits[elem[1]][4],edg[elem[1]+1]),(inits[elem[2]][4],edg[elem[2]+1]),(inits[elem[3]][4],edg[elem[3]+1])]])
                nxor05 = nxor05 + 1
    k=k+1
    if k % 200 == 0:
    # odometer...
        print(k)

workbook = xlwt.Workbook(encoding='utf8')
worksheet = workbook.add_sheet('NOT gates')

worksheet.write(0,0,"NOT gates")
worksheet.write(0,1,len(found_not))
worksheet.write(0,2,"List of first 20000 rows, not redundant")
i=1
worksheet.write(i,0,"N.found with threshold 2:")
worksheet.write(i,1,nnot2)
i=i+1
worksheet.write(i,0,"N.found with threshold 1:")
worksheet.write(i,1,nnot1)
i=i+1
worksheet.write(i,0,"N.found with threshold .5:")
worksheet.write(i,1,nnot05)
i=i+1
worksheet.write(i,0,"Edge")
worksheet.write(i,1,"Threshold")
worksheet.write(i,2,"Input bit")
worksheet.write(i,3,"Input state")
worksheet.write(i,4,"Output")

pre_gat = ""
pre_bit = ""
other_states = False
for gate in found_not:
    if gate[0] == pre_gat and gate[2] == pre_bit:
        if not other_states:
            worksheet.write(i,5,"Equivalent input states")
            other_states = True
        #continue
    other_states = False
    pre_gat = gate[0]
    pre_bit = gate[2]
    i=i+1
    worksheet.write(i,0,gate[0])
    worksheet.write(i,1,gate[1])
    worksheet.write(i,2,gate[2])
    worksheet.write(i,3,gate[3][0][0])
    worksheet.write(i,4,gate[3][0][1])
    i=i+1
    worksheet.write(i,3,gate[3][1][0])
    worksheet.write(i,4,gate[3][1][1])
    if i>20000:
        break


worksheett = workbook.add_sheet('OR gates')
worksheett.write(0,0,"OR gates")
worksheett.write(0,1,len(found_or))
worksheett.write(0,2,"List of first 20000 rows, not redundant")
i=1
worksheett.write(i,0,"N.found with threshold 2:")
worksheett.write(i,1,nor2)
i=i+1
worksheett.write(i,0,"N.found with threshold 1:")
worksheett.write(i,1,nor1)
i=i+1
worksheett.write(i,0,"N.found with threshold .5:")
worksheett.write(i,1,nor05)
i=i+1
worksheett.write(i,0,"Edge")
worksheett.write(i,1,"Threshold")
worksheett.write(i,2,"Input bits")
worksheett.write(i,3,"Input state")
worksheett.write(i,4,"Output")

pre_gat = ""
pre_bit = ""
other_states = False
for gate in found_or:
    if gate[0] == pre_gat and gate[2] == pre_bit:
        if not other_states:
            worksheett.write(i,5,"Other equivalent input states too")
            other_states = True
        #continue
    other_states = False
    pre_gat = gate[0]
    pre_bit = gate[2]
    i=i+1
    worksheett.write(i,0,gate[0])
    worksheett.write(i,1,gate[1])
    worksheett.write(i,2,gate[2])
    worksheett.write(i,3,gate[3][0][0])
    worksheett.write(i,4,gate[3][0][1])
    i=i+1
    worksheett.write(i,3,gate[3][1][0])
    worksheett.write(i,4,gate[3][1][1])
    i=i+1
    worksheett.write(i,3,gate[3][2][0])
    worksheett.write(i,4,gate[3][2][1])
    i=i+1
    worksheett.write(i,3,gate[3][3][0])
    worksheett.write(i,4,gate[3][3][1])
    if i>20000:
        break


worksheett1 = workbook.add_sheet('AND gates')
worksheett1.write(0,0,"AND gates")
worksheett1.write(0,1,len(found_and))
worksheett1.write(0,2,"List of first 20000 rows, not redundant")
i=1
worksheett1.write(i,0,"N.found with threshold 2:")
worksheett1.write(i,1,nand2)
i=i+1
worksheett1.write(i,0,"N.found with threshold 1:")
worksheett1.write(i,1,nand1)
i=i+1
worksheett1.write(i,0,"N.found with threshold .5:")
worksheett1.write(i,1,nand05)
i=i+1
worksheett1.write(i,0,"Edge")
worksheett1.write(i,1,"Threshold")
worksheett1.write(i,2,"Input bits")
worksheett1.write(i,3,"Input state")
worksheett1.write(i,4,"Output")

pre_gat = ""
pre_bit = ""
other_states = False
for gate in found_and:
    if gate[0] == pre_gat and gate[2] == pre_bit:
        if not other_states:
            worksheett1.write(i,5,"Other equivalent input states too")
            other_states = True
        #continue
    other_states = False
    pre_gat = gate[0]
    pre_bit = gate[2]
    i=i+1
    worksheett1.write(i,0,gate[0])
    worksheett1.write(i,1,gate[1])
    worksheett1.write(i,2,gate[2])
    worksheett1.write(i,3,gate[3][0][0])
    worksheett1.write(i,4,gate[3][0][1])
    i=i+1
    worksheett1.write(i,3,gate[3][1][0])
    worksheett1.write(i,4,gate[3][1][1])
    i=i+1
    worksheett1.write(i,3,gate[3][2][0])
    worksheett1.write(i,4,gate[3][2][1])
    i=i+1
    worksheett1.write(i,3,gate[3][3][0])
    worksheett1.write(i,4,gate[3][3][1])
    if i>20000:
        break

worksheett2 = workbook.add_sheet('XOR gates')
worksheett2.write(0,0,"XOR gates")
worksheett2.write(0,1,len(found_xor))
worksheett2.write(0,2,"List of first 20000 rows, not redundant")
i=1
worksheett2.write(i,0,"N.found with threshold 2:")
worksheett2.write(i,1,nxor2)
i=i+1
worksheett2.write(i,0,"N.found with threshold 1:")
worksheett2.write(i,1,nxor1)
i=i+1
worksheett2.write(i,0,"N.found with threshold .5:")
worksheett2.write(i,1,nxor05)
i=i+1
worksheett2.write(i,0,"Edge")
worksheett2.write(i,1,"Threshold")
worksheett2.write(i,2,"Input bits")
worksheett2.write(i,3,"Input state")
worksheett2.write(i,4,"Output")

pre_gat = ""
pre_bit = ""
other_states = False
for gate in found_xor:
    if gate[0] == pre_gat and gate[2] == pre_bit:
        if not other_states:
            worksheett2.write(i,5,"Other equivalent input states too")
            other_states = True
        #continue
    other_states = False
    pre_gat = gate[0]
    pre_bit = gate[2]
    i=i+1
    worksheett2.write(i,0,gate[0])
    worksheett2.write(i,1,gate[1])
    worksheett2.write(i,2,gate[2])
    worksheett2.write(i,3,gate[3][0][0])
    worksheett2.write(i,4,gate[3][0][1])
    i=i+1
    worksheett2.write(i,3,gate[3][1][0])
    worksheett2.write(i,4,gate[3][1][1])
    i=i+1
    worksheett2.write(i,3,gate[3][2][0])
    worksheett2.write(i,4,gate[3][2][1])
    i=i+1
    worksheett2.write(i,3,gate[3][3][0])
    worksheett2.write(i,4,gate[3][3][1])
    if i>20000:
        break

workbook.save('data/found_gates'+fname+'.xls')
