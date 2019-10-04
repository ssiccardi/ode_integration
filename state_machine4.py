# this program reads states_x.csv with the states of some edges, then computes the state table for all the possible combinations
# of 4 edges, given the input state table inits_ok4.csv
# presently is in a simple form, for 11 edges only
# output in state_table_x.xls

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

inits = list(csv.reader(open('data/inits_ok4.csv'), delimiter=","))

states = list(csv.reader(open('data/states'+fname+'.csv'), delimiter=","))
inistat = []
for ini in inits:
    tmp=""
    i = 0
    for ini1 in ini:
        tmp=tmp+ini1
    inistat.append(tmp)

combinations = [
"abcd","abce","abcf","abcg","abch","abci","abcj","abck","abde","abdf","abdg","abdh","abdi","abdj","abdk","abef","abeg","abeh","abei","abej","abek","abfg","abfh","abfi","abfj","abfk","abgh","abgi","abgj",
"abgk","abhi","abhj","abhk","abij","abik","abjk","acde","acdf","acdg","acdh","acdi","acdj","acdk","acef","aceg","aceh","acei","acej","acek","acfg","acfh","acfi","acfj","acfk","acgh","acgi","acgj","acgk",
"achi","achj","achk","acij","acik","acjk","adef","adeg","adeh","adei","adej","adek","adfg","adfh","adfi","adfj","adfk","adgh","adgi","adgj","adgk","adhi","adhj","adhk","adij","adik","adjk","aefg","aefh",
"aefi","aefj","aefk","aegh","aegi","aegj","aegk","aehi","aehj","aehk","aeij","aeik","aejk","afgh","afgi","afgj","afgk","afhi","afhj","afhk","afij","afik","afjk","aghi","aghj","aghk","agij","agik","agjk",
"ahij","ahik","ahjk","aijk","bcde","bcdf","bcdg","bcdh","bcdi","bcdj","bcdk","bcef","bceg","bceh","bcei","bcej","bcek","bcfg","bcfh","bcfi","bcfj","bcfk","bcgh","bcgi","bcgj","bcgk","bchi","bchj","bchk",
"bcij","bcik","bcjk","bdef","bdeg","bdeh","bdei","bdej","bdek","bdfg","bdfh","bdfi","bdfj","bdfk","bdgh","bdgi","bdgj","bdgk","bdhi","bdhj","bdhk","bdij","bdik","bdjk","befg","befh","befi","befj","befk",
"begh","begi","begj","begk","behi","behj","behk","beij","beik","bejk","bfgh","bfgi","bfgj","bfgk","bfhi","bfhj","bfhk","bfij","bfik","bfjk","bghi","bghj","bghk","bgij","bgik","bgjk","bhij","bhik","bhjk",
"bijk","cdef","cdeg","cdeh","cdei","cdej","cdek","cdfg","cdfh","cdfi","cdfj","cdfk","cdgh","cdgi","cdgj","cdgk","cdhi","cdhj","cdhk","cdij","cdik","cdjk","cefg","cefh","cefi","cefj","cefk","cegh","cegi",
"cegj","cegk","cehi","cehj","cehk","ceij","ceik","cejk","cfgh","cfgi","cfgj","cfgk","cfhi","cfhj","cfhk","cfij","cfik","cfjk","cghi","cghj","cghk","cgij","cgik","cgjk","chij","chik","chjk","cijk","defg",
"defh","defi","defj","defk","degh","degi","degj","degk","dehi","dehj","dehk","deij","deik","dejk","dfgh","dfgi","dfgj","dfgk","dfhi","dfhj","dfhk","dfij","dfik","dfjk","dghi","dghj","dghk","dgij","dgik",
"dgjk","dhij","dhik","dhjk","dijk","efgh","efgi","efgj","efgk","efhi","efhj","efhk","efij","efik","efjk","eghi","eghj","eghk","egij","egik","egjk","ehij","ehik","ehjk","eijk","fghi","fghj","fghk","fgij",
"fgik","fgjk","fhij","fhik","fhjk","fijk","ghij","ghik","ghjk","gijk","hijk"
]
# from http://utenti.quipo.it/base5/combinatoria/calcombinat.htm

prob_machine = []
for i in range(16):
    tmp = []
    for i in range(16):
        tmp.append(0)
    prob_machine.append(tmp)
tstates = len(combinations)
    
workbook = xlwt.Workbook(encoding='utf8')
worksheet = workbook.add_sheet('State tables')

worksheet.write(0,0,"Input N.")
worksheet.write(0,1,"Input states")
worksheet.write(0,2,"Output states")

r = 2
m = 1
for combi in combinations:
    edges = []
    for i in range(4):
        edges.append("abcdefghijk".index(combi[i:i+1]))
    worksheet.write(r,0,"Machine n. %s" %m)
    r=r+1
    s=1
    for status in inistat:
        worksheet.write(r,0,s)
        worksheet.write(r,1,status)
        tmp = ""
        for edge in edges:
            tmp = tmp + states[edge][1][s-1:s]
        worksheet.write(r,2,tmp)
        prob_machine[inistat.index(status)][inistat.index(tmp)] = prob_machine[inistat.index(status)][inistat.index(tmp)] + 1
        s=s+1
        r=r+1
    m=m+1
    r=r+2

worksheet = workbook.add_sheet('Probab. Machine')

worksheet.write(0,0,"Input State")
worksheet.write(0,1,"Output State")
worksheet.write(0,2,"Frequency")
worksheet.write(0,3,"Cumulated Frequency")

r = 2
for i in range(16):
    cumul = 0
    for k in range(16):
        worksheet.write(r,0,inistat[i])
        worksheet.write(r,1,inistat[k])
        worksheet.write(r,2,prob_machine[i][k]/tstates)
        cumul = cumul + prob_machine[i][k]/tstates
        worksheet.write(r,3,cumul)
        r = r + 1

workbook.save('data/state_table'+fname+'.xls')
