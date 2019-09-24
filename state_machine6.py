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

inits = list(csv.reader(open('data/inits_ok6.csv'), delimiter=","))

states = list(csv.reader(open('data/states'+fname+'.csv'), delimiter=","))
inistat = []
for ini in inits:
    tmp=""
    i = 0
    for ini1 in ini:
        tmp=tmp+ini1
    inistat.append(tmp)

combinations = [
"abcdef","abcdeg","abcdeh","abcdei","abcdej","abcdek","abcdfg","abcdfh","abcdfi","abcdfj","abcdfk","abcdgh","abcdgi",
"abcdgj","abcdgk","abcdhi","abcdhj","abcdhk","abcdij","abcdik","abcdjk","abcefg","abcefh","abcefi","abcefj","abcefk",
"abcegh","abcegi","abcegj","abcegk","abcehi","abcehj","abcehk","abceij","abceik","abcejk","abcfgh","abcfgi","abcfgj",
"abcfgk","abcfhi","abcfhj","abcfhk","abcfij","abcfik","abcfjk","abcghi","abcghj","abcghk","abcgij","abcgik","abcgjk",
"abchij","abchik","abchjk","abcijk","abdefg","abdefh","abdefi","abdefj","abdefk","abdegh","abdegi","abdegj","abdegk",
"abdehi","abdehj","abdehk","abdeij","abdeik","abdejk","abdfgh","abdfgi","abdfgj","abdfgk","abdfhi","abdfhj","abdfhk",
"abdfij","abdfik","abdfjk","abdghi","abdghj","abdghk","abdgij","abdgik","abdgjk","abdhij","abdhik","abdhjk","abdijk",
"abefgh","abefgi","abefgj","abefgk","abefhi","abefhj","abefhk","abefij","abefik","abefjk","abeghi","abeghj","abeghk",
"abegij","abegik","abegjk","abehij","abehik","abehjk","abeijk","abfghi","abfghj","abfghk","abfgij","abfgik","abfgjk",
"abfhij","abfhik","abfhjk","abfijk","abghij","abghik","abghjk","abgijk","abhijk","acdefg","acdefh","acdefi","acdefj",
"acdefk","acdegh","acdegi","acdegj","acdegk","acdehi","acdehj","acdehk","acdeij","acdeik","acdejk","acdfgh","acdfgi",
"acdfgj","acdfgk","acdfhi","acdfhj","acdfhk","acdfij","acdfik","acdfjk","acdghi","acdghj","acdghk","acdgij","acdgik",
"acdgjk","acdhij","acdhik","acdhjk","acdijk","acefgh","acefgi","acefgj","acefgk","acefhi","acefhj","acefhk","acefij",
"acefik","acefjk","aceghi","aceghj","aceghk","acegij","acegik","acegjk","acehij","acehik","acehjk","aceijk","acfghi",
"acfghj","acfghk","acfgij","acfgik","acfgjk","acfhij","acfhik","acfhjk","acfijk","acghij","acghik","acghjk","acgijk",
"achijk","adefgh","adefgi","adefgj","adefgk","adefhi","adefhj","adefhk","adefij","adefik","adefjk","adeghi","adeghj",
"adeghk","adegij","adegik","adegjk","adehij","adehik","adehjk","adeijk","adfghi","adfghj","adfghk","adfgij","adfgik",
"adfgjk","adfhij","adfhik","adfhjk","adfijk","adghij","adghik","adghjk","adgijk","adhijk","aefghi","aefghj","aefghk",
"aefgij","aefgik","aefgjk","aefhij","aefhik","aefhjk","aefijk","aeghij","aeghik","aeghjk","aegijk","aehijk","afghij",
"afghik","afghjk","afgijk","afhijk","aghijk","bcdefg","bcdefh","bcdefi","bcdefj","bcdefk","bcdegh","bcdegi","bcdegj",
"bcdegk","bcdehi","bcdehj","bcdehk","bcdeij","bcdeik","bcdejk","bcdfgh","bcdfgi","bcdfgj","bcdfgk","bcdfhi","bcdfhj",
"bcdfhk","bcdfij","bcdfik","bcdfjk","bcdghi","bcdghj","bcdghk","bcdgij","bcdgik","bcdgjk","bcdhij","bcdhik","bcdhjk",
"bcdijk","bcefgh","bcefgi","bcefgj","bcefgk","bcefhi","bcefhj","bcefhk","bcefij","bcefik","bcefjk","bceghi","bceghj",
"bceghk","bcegij","bcegik","bcegjk","bcehij","bcehik","bcehjk","bceijk","bcfghi","bcfghj","bcfghk","bcfgij","bcfgik",
"bcfgjk","bcfhij","bcfhik","bcfhjk","bcfijk","bcghij","bcghik","bcghjk","bcgijk","bchijk","bdefgh","bdefgi","bdefgj",
"bdefgk","bdefhi","bdefhj","bdefhk","bdefij","bdefik","bdefjk","bdeghi","bdeghj","bdeghk","bdegij","bdegik","bdegjk",
"bdehij","bdehik","bdehjk","bdeijk","bdfghi","bdfghj","bdfghk","bdfgij","bdfgik","bdfgjk","bdfhij","bdfhik","bdfhjk",
"bdfijk","bdghij","bdghik","bdghjk","bdgijk","bdhijk","befghi","befghj","befghk","befgij","befgik","befgjk","befhij",
"befhik","befhjk","befijk","beghij","beghik","beghjk","begijk","behijk","bfghij","bfghik","bfghjk","bfgijk","bfhijk",
"bghijk","cdefgh","cdefgi","cdefgj","cdefgk","cdefhi","cdefhj","cdefhk","cdefij","cdefik","cdefjk","cdeghi","cdeghj",
"cdeghk","cdegij","cdegik","cdegjk","cdehij","cdehik","cdehjk","cdeijk","cdfghi","cdfghj","cdfghk","cdfgij","cdfgik",
"cdfgjk","cdfhij","cdfhik","cdfhjk","cdfijk","cdghij","cdghik","cdghjk","cdgijk","cdhijk","cefghi","cefghj","cefghk",
"cefgij","cefgik","cefgjk","cefhij","cefhik","cefhjk","cefijk","ceghij","ceghik","ceghjk","cegijk","cehijk","cfghij",
"cfghik","cfghjk","cfgijk","cfhijk","cghijk","defghi","defghj","defghk","defgij","defgik","defgjk","defhij","defhik",
"defhjk","defijk","deghij","deghik","deghjk","degijk","dehijk","dfghij","dfghik","dfghjk","dfgijk","dfhijk","dghijk",
"efghij","efghik","efghjk","efgijk","efhijk","eghijk","fghijk"
]
# from http://utenti.quipo.it/base5/combinatoria/calcombinat.htm

workbook = xlwt.Workbook(encoding='utf8')
worksheet = workbook.add_sheet('State tables')

worksheet.write(0,0,"Input N.")
worksheet.write(0,1,"Input states")
worksheet.write(0,2,"Output states")

r = 2
m = 1
for combi in combinations:
    edges = []
    for i in range(6):
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
        s=s+1
        r=r+1
    m=m+1
    r=r+2


workbook.save('data/state_table'+fname+'.xls')
