import csv
import re

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

fobj = csv.writer(open('filterdata.csv','wb'),delimiter=',')
with open('Taxfinaldata.csv','rb') as mf:
    rows = csv.reader(mf)
    fobj.writerow(rows.next())
    for ctr,row in enumerate(rows,start=0):
        if not any(('REAL EST' or 'REAL ESTATE') in s for s in row) and not any('LLC' in s for s in row):
            fobj.writerow(row)
            print ctr
            continue
            for x in row:
                word = findWholeWord('EST')(x)
                if word:
                    flag = True
            if flag:
                fobj.writerow(row)
            flag = False
            
