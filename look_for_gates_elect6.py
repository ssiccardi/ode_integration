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
(optlist, args) = parser.parse_args()

if not optlist.fname:
    fname = ""
else:
    fname = "_"+optlist.fname

check_not = []
check_others = []
nstates = 6
inits = list(csv.reader(open('data/inits_ok6.csv'), delimiter=","))
check_not.append([6,[(63,64),(61,62),(59,60),(57,58),(55,56),(53,54),(51,52),(49,50),(47,48),(45,46),(43,44),(41,42),(39,40),(37,38),(35,36),(33,34),(31,32),(29,30),(27,28),(25,26),(23,24),(21,22),(19,20),(17,18),(15,16),(13,14),(11,12),(9,10),(7,8),(5,6),(3,4),(1,2)]])
check_not.append([5,[(64,62),(63,61),(60,58),(59,57),(56,54),(55,53),(52,50),(51,49),(48,46),(47,45),(44,42),(43,41),(40,38),(39,37),(36,34),(35,33),(32,30),(31,29),(28,26),(27,25),(24,22),(23,21),(20,18),(19,17),(16,14),(15,13),(12,10),(11,9),(8,6),(7,5),(4,2),(3,1)]])
check_not.append([4,[(64,60),(63,59),(62,58),(61,57),(56,52),(55,51),(54,50),(53,49),(48,44),(47,43),(46,42),(45,41),(40,36),(39,35),(38,34),(37,33),(32,28),(31,27),(30,26),(29,25),(24,20),(23,19),(22,18),(21,17),(16,12),(15,11),(14,10),(13,9),(8,4),(7,3),(6,2),(5,1)]])
check_not.append([3,[(64,56),(63,55),(62,54),(61,53),(60,52),(59,51),(58,50),(57,49),(48,40),(47,39),(46,38),(45,37),(44,36),(43,35),(42,34),(41,33),(32,24),(31,23),(30,22),(29,21),(28,20),(27,19),(26,18),(25,17),(16,8),(15,7),(14,6),(13,5),(12,4),(11,3),(10,2),(9,1)]])
check_not.append([2,[(64,48),(63,47),(62,46),(61,45),(60,44),(59,43),(58,42),(57,41),(56,40),(55,39),(54,38),(53,37),(52,36),(51,35),(50,34),(49,33),(32,16),(31,15),(30,14),(29,13),(28,12),(27,11),(26,10),(25,9),(24,8),(23,7),(22,6),(21,5),(20,4),(19,3),(18,2),(17,1)]])
check_not.append([1,[(64,32),(63,31),(62,30),(61,29),(60,28),(59,27),(58,26),(57,25),(56,24),(55,23),(54,22),(53,21),(52,20),(51,19),(50,18),(49,17),(48,16),(47,15),(46,14),(45,13),(44,12),(43,11),(42,10),(41,9),(40,8),(39,7),(38,6),(37,5),(36,4),(35,3),(34,2),(33,1)]])

check_others.append([(1,2),[(64,32,48,16),(63,31,47,15),(62,30,46,14),(61,29,45,13),(60,28,44,12),(59,27,43,11),(58,26,42,10),(57,25,41,9),(56,24,40,8),(55,23,39,7),(54,22,38,6),(53,21,37,5),(52,20,36,4),(51,19,35,3),(50,18,34,2),(49,17,33,1)],"1-2"])
check_others.append([(1,3),[(64,32,56,24),(63,31,55,23),(62,30,54,22),(61,29,53,21),(60,28,52,20),(59,27,51,19),(58,26,50,18),(57,25,49,17),(48,16,40,8),(47,15,39,7),(46,14,38,6),(45,13,37,5),(44,12,36,4),(43,11,35,3),(42,10,34,2),(41,9,33,1)],'1-3'])
check_others.append([(1,4),[(64,32,60,28),(63,31,59,27),(62,30,58,26),(61,29,57,25),(56,24,52,20),(55,23,51,19),(54,22,50,18),(53,21,49,17),(48,16,44,12),(47,15,43,11),(46,14,42,10),(45,13,41,9),(40,8,36,4),(39,7,35,3),(38,6,34,2),(37,5,33,1)],'1-4'])
check_others.append([(1,5),[(64,32,62,30),(63,31,61,29),(60,28,58,26),(59,27,57,25),(56,24,54,22),(55,23,53,21),(52,20,50,18),(51,19,49,17),(48,16,46,14),(47,15,45,13),(44,12,42,10),(43,11,41,9),(40,8,38,6),(39,7,37,5),(36,4,34,2),(35,3,33,1)],'1-5'])
check_others.append([(1,6),[(64,32,63,31),(62,30,61,29),(60,28,59,27),(58,26,57,25),(56,24,55,23),(54,22,53,21),(52,20,51,19),(50,18,49,17),(48,16,47,15),(46,14,45,13),(44,12,43,11),(42,10,41,9),(40,8,39,7),(38,6,37,5),(36,4,35,3),(34,2,33,1)],'1-6'])
check_others.append([(2,3),[(64,56,48,40),(63,55,47,39),(62,54,46,38),(61,53,45,37),(60,52,44,36),(59,51,43,35),(58,50,42,34),(57,49,41,33),(32,24,16,8),(31,23,15,7),(30,22,14,6),(29,21,13,5),(28,20,12,4),(27,19,11,3),(26,18,10,2),(25,17,9,1)],'2-3'])
check_others.append([(2,4),[(64,48,60,44),(63,47,59,43),(62,46,58,42),(61,45,57,41),(56,40,52,36),(55,39,51,35),(54,38,50,34),(53,37,49,33),(32,16,28,12),(31,15,27,11),(30,14,26,10),(29,13,25,9),(24,8,20,4),(23,7,19,3),(22,6,18,2),(21,5,17,1)],'2-4'])
check_others.append([(2,5),[(64,48,62,46),(63,47,61,45),(60,44,58,42),(59,43,57,41),(56,40,54,38),(55,39,53,37),(52,36,50,34),(51,35,49,33),(32,16,30,14),(31,15,29,13),(28,12,26,10),(27,11,25,9),(24,8,22,6),(23,7,21,5),(20,4,18,2),(19,3,17,1)],'2-5'])
check_others.append([(2,6),[(64,48,63,47),(62,46,61,45),(60,44,59,43),(58,42,57,41),(56,40,55,39),(54,38,53,37),(52,36,51,35),(50,34,49,33),(32,16,31,15),(30,14,29,13),(28,12,27,11),(26,10,25,9),(24,8,23,7),(22,6,21,5),(20,4,19,3),(18,2,17,1)],'2-6'])
check_others.append([(3,4),[(64,60,56,52),(63,59,55,51),(62,58,54,50),(61,57,53,49),(48,44,40,36),(47,43,39,35),(46,42,38,34),(45,41,37,33),(32,28,24,20),(31,27,23,19),(30,26,22,18),(29,25,21,17),(16,12,8,4),(15,11,7,3),(14,10,6,2),(13,9,5,1)],'3-4'])
check_others.append([(3,5),[(64,56,62,54),(63,55,61,53),(60,52,58,50),(59,51,57,49),(48,40,46,38),(47,39,45,37),(44,36,42,34),(43,35,41,33),(32,24,30,22),(31,23,29,21),(28,20,26,18),(27,19,25,17),(16,8,14,6),(15,7,13,5),(12,4,10,2),(11,3,9,1)],'3-5'])
check_others.append([(3,6),[(64,56,63,55),(62,54,61,53),(60,52,59,51),(58,50,57,49),(48,40,47,39),(46,38,45,37),(44,36,43,35),(42,34,41,33),(32,24,31,23),(30,22,29,21),(28,20,27,19),(26,18,25,17),(16,8,15,7),(14,6,13,5),(12,4,11,3),(10,2,9,1)],'3-6'])
check_others.append([(4,5),[(64,62,60,58),(63,61,59,57),(56,54,52,50),(55,53,51,49),(48,46,44,42),(47,45,43,41),(40,38,36,34),(39,37,35,33),(32,30,28,26),(31,29,27,25),(24,22,20,18),(23,21,19,17),(16,14,12,10),(15,13,11,9),(8,6,4,2),(7,5,3,1)],'4-5'])
check_others.append([(4,6),[(64,60,63,59),(62,58,61,57),(56,52,55,51),(54,50,53,49),(48,44,47,43),(46,42,45,41),(40,36,39,35),(38,34,37,33),(32,28,31,27),(30,26,29,25),(24,20,23,19),(22,18,21,17),(16,12,15,11),(14,10,13,9),(8,4,7,3),(6,2,5,1)],'4-6'])
check_others.append([(5,6),[(64,63,62,61),(60,59,58,57),(56,55,54,53),(52,51,50,49),(48,47,46,45),(44,43,42,41),(40,39,38,37),(36,35,34,33),(32,31,30,29),(28,27,26,25),(24,23,22,21),(20,19,18,17),(16,15,14,13),(12,11,10,9),(8,7,6,5),(4,3,2,1)],'5-6'])

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
            if inits[elem[0]-1][bc] != int(edg[elem[0]-1+129]) and inits[elem[1]-1][bc] != int(edg[elem[1]-1+129]):
                found_not.append([edg[0],2.0,bc+1,[(inits[elem[0]-1][4],edg[elem[0]-1+129]),(inits[elem[1]-1][4],edg[elem[1]-1+129])]])
                nnot2 = nnot2 + 1
                #continue
            if inits[elem[0]-1][bc] != int(edg[elem[0]-1+65]) and inits[elem[1]-1][bc] != int(edg[elem[1]-1+65]):
                found_not.append([edg[0],1.0,bc+1,[(inits[elem[0]-1][4],edg[elem[0]-1+65]),(inits[elem[1]-1][4],edg[elem[1]-1+65])]])
                nnot1 = nnot1 + 1
                #continue
            if inits[elem[0]-1][bc] != int(edg[elem[0]]) and inits[elem[1]-1][bc] != int(edg[elem[1]]):
                found_not.append([edg[0],0.5,bc+1,[(inits[elem[0]-1][4],edg[elem[0]]),(inits[elem[1]-1][4],edg[elem[1]])]])
                nnot05 = nnot05 + 1

    for tocheck in check_others:
        bc1 = tocheck[0][0]-1
        bc2 = tocheck[0][1]-1
        for elem in tocheck[1]:
        # OR
            if (inits[elem[0]-1][bc1] or inits[elem[0]-1][bc2]) == int(edg[elem[0]-1+129]) and (inits[elem[1]-1][bc1] or inits[elem[1]-1][bc2]) == int(edg[elem[1]-1+129]) and \
                (inits[elem[2]-1][bc1] or inits[elem[2]-1][bc2]) == int(edg[elem[2]-1+129]) and (inits[elem[3]-1][bc1] or inits[elem[3]-1][bc2]) == int(edg[elem[3]-1+129]):
                found_or.append([edg[0],2.0,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+129]),(inits[elem[1]-1][4],edg[elem[1]-1+129]),(inits[elem[2]-1][4],edg[elem[2]-1+129]),(inits[elem[3]-1][4],edg[elem[3]-1+129])]])
                nor2 = nor2 + 1
            if (inits[elem[0]-1][bc1] or inits[elem[0]-1][bc2]) == int(edg[elem[0]-1+65]) and (inits[elem[1]-1][bc1] or inits[elem[1]-1][bc2]) == int(edg[elem[1]-1+65]) and \
                (inits[elem[2]-1][bc1] or inits[elem[2]-1][bc2]) == int(edg[elem[2]-1+65]) and (inits[elem[3]-1][bc1] or inits[elem[3]-1][bc2]) == int(edg[elem[3]-1+65]):
                found_or.append([edg[0],1.0,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+65]),(inits[elem[1]-1][4],edg[elem[1]-1+65]),(inits[elem[2]-1][4],edg[elem[2]-1+65]),(inits[elem[3]-1][4],edg[elem[3]-1+65])]])
                nor1 = nor1 + 1
            if (inits[elem[0]-1][bc1] or inits[elem[0]-1][bc2]) == int(edg[elem[0]-1+1]) and  (inits[elem[1]-1][bc1] or inits[elem[1]-1][bc2]) == int(edg[elem[1]-1+1]) and \
                (inits[elem[2]-1][bc1] or inits[elem[2]-1][bc2]) == int(edg[elem[2]-1+1]) and (inits[elem[3]-1][bc1] or inits[elem[3]-1][bc2]) == int(edg[elem[3]-1+1]):
                found_or.append([edg[0],0.5,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+1]),(inits[elem[1]-1][4],edg[elem[1]-1+1]),(inits[elem[2]-1][4],edg[elem[2]-1+1]),(inits[elem[3]-1][4],edg[elem[3]-1+1])]])
                nor05 = nor05 + 1
        # AND
            if (inits[elem[0]-1][bc1] and inits[elem[0]-1][bc2]) == int(edg[elem[0]-1+129]) and (inits[elem[1]-1][bc1] and inits[elem[1]-1][bc2]) == int(edg[elem[1]-1+129]) and \
                (inits[elem[2]-1][bc1] and inits[elem[2]-1][bc2]) == int(edg[elem[2]-1+129]) and (inits[elem[3]-1][bc1] and inits[elem[3]-1][bc2]) == int(edg[elem[3]-1+129]):
                found_and.append([edg[0],2.0,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+129]),(inits[elem[1]-1][4],edg[elem[1]-1+129]),(inits[elem[2]-1][4],edg[elem[2]-1+129]),(inits[elem[3]-1][4],edg[elem[3]-1+129])]])
                nand2 = nand2 + 1
            if (inits[elem[0]-1][bc1] and inits[elem[0]-1][bc2]) == int(edg[elem[0]-1+65]) and (inits[elem[1]-1][bc1] and inits[elem[1]-1][bc2]) == int(edg[elem[1]-1+65]) and \
                (inits[elem[2]-1][bc1] and inits[elem[2]-1][bc2]) == int(edg[elem[2]-1+65]) and (inits[elem[3]-1][bc1] and inits[elem[3]-1][bc2]) == int(edg[elem[3]-1+65]):
                found_and.append([edg[0],1.0,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+65]),(inits[elem[1]-1][4],edg[elem[1]-1+65]),(inits[elem[2]-1][4],edg[elem[2]-1+65]),(inits[elem[3]-1][4],edg[elem[3]-1+65])]])
                nand1 = nand1 + 1
            if (inits[elem[0]-1][bc1] and inits[elem[0]-1][bc2]) == int(edg[elem[0]-1+1]) and (inits[elem[1]-1][bc1] and inits[elem[1]-1][bc2]) == int(edg[elem[1]-1+1]) and \
                (inits[elem[2]-1][bc1] and inits[elem[2]-1][bc2]) == int(edg[elem[2]-1+1]) and (inits[elem[3]-1][bc1] and inits[elem[3]-1][bc2]) == int(edg[elem[3]-1+1]):
                found_and.append([edg[0],0.5,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+1]),(inits[elem[1]-1][4],edg[elem[1]-1+1]),(inits[elem[2]-1][4],edg[elem[2]-1+1]),(inits[elem[3]-1][4],edg[elem[3]-1+1])]])
                nand05 = nand05 + 1
        # XOR
            if ((inits[elem[0]-1][bc1] + inits[elem[0]-1][bc2])%2) == int(edg[elem[0]-1+129]) and ((inits[elem[1]-1][bc1] + inits[elem[1]-1][bc2])%2) == int(edg[elem[1]-1+129]) and \
                ((inits[elem[2]-1][bc1] + inits[elem[2]-1][bc2])%2) == int(edg[elem[2]-1+129]) and ((inits[elem[3]-1][bc1] + inits[elem[3]-1][bc2])%2) == int(edg[elem[3]-1+129]):
                found_xor.append([edg[0],2.0,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+129]),(inits[elem[1]-1][4],edg[elem[1]-1+129]),(inits[elem[2]-1][4],edg[elem[2]-1+129]),(inits[elem[3]-1][4],edg[elem[3]-1+129])]])
                nxor2 = nxor2 + 1
            if ((inits[elem[0]-1][bc1] + inits[elem[0]-1][bc2])%2) == int(edg[elem[0]-1+65]) and ((inits[elem[1]-1][bc1] + inits[elem[1]-1][bc2])%2) == int(edg[elem[1]-1+65]) and \
                ((inits[elem[2]-1][bc1] + inits[elem[2]-1][bc2])%2) == int(edg[elem[2]-1+65]) and ((inits[elem[3]-1][bc1] + inits[elem[3]-1][bc2])%2) == int(edg[elem[3]-1+65]):
                found_xor.append([edg[0],1.0,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+65]),(inits[elem[1]-1][4],edg[elem[1]-1+65]),(inits[elem[2]-1][4],edg[elem[2]-1+65]),(inits[elem[3]-1][4],edg[elem[3]-1+65])]])
                nxor1 = nxor1 + 1
            if ((inits[elem[0]-1][bc1] + inits[elem[0]-1][bc2])%2) == int(edg[elem[0]-1+1]) and ((inits[elem[1]-1][bc1] + inits[elem[1]-1][bc2])%2) == int(edg[elem[1]-1+1]) and \
                ((inits[elem[2]-1][bc1] + inits[elem[2]-1][bc2])%2) == int(edg[elem[2]-1+1]) and ((inits[elem[3]-1][bc1] + inits[elem[3]-1][bc2])%2) == int(edg[elem[3]-1+1]):
                found_xor.append([edg[0],0.5,tocheck[2],[(inits[elem[0]-1][4],edg[elem[0]-1+1]),(inits[elem[1]-1][4],edg[elem[1]-1+1]),(inits[elem[2]-1][4],edg[elem[2]-1+1]),(inits[elem[3]-1][4],edg[elem[3]-1+1])]])
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
            worksheett.write(i,5,"Equivalent input states")
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
            worksheett1.write(i,5,"Equivalent input states")
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
            worksheett2.write(i,5,"Equivalent input states")
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
