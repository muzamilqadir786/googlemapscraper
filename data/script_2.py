import zipfile

import os
from setuptools.command.sdist import re_finder


##for root, dirs, files in os.walk(base_dir):
##    for file1 in files:
##        print '---', file
##        fh = open(base_dir+file1, 'rb')
##        z = zipfile.ZipFile(fh)
##        for name in z.namelist():
##            outpath = "C:\\files"
##            z.extract(name, outpath)
    

"""
Getting COL names as 1st  line in final csv file
"""
import csv
f = open('c://files/0702monm151310.csv','rb')
r = csv.reader(f)
fline = r.next()

"""
Getting all csv files from c://files
"""
import re
base_dir = "c://files/"
for root, dirs, files in os.walk(base_dir):
    csv_files = [fi for fi in files if fi.endswith(".csv") ]

csv_files = filter(None,[el if re.match('^\d{4}',el) else None for el in csv_files])
print csv_files
print len(csv_files)


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


total_rows = 0
est_csv = open(base_dir+'Real_estatesdatan12.csv','wb')
fobj = csv.writer(est_csv,delimiter=',')
fobj.writerow(fline)
flag = False
for csv_file in csv_files:
    print csv_file
    with open(base_dir+csv_file,'rb',0) as f:
        rows = csv.reader(f)

        for ctr,row in enumerate(rows,start=0):
            if not (('REAL EST' or 'REAL ESTATE') in row[6]) and any('ESTATE' in a for a in row) and not any('LLC' in s for s in row):
##            if any('LLC' in s for s in row):
                fobj.writerow(row.append(csv_file))
                print ctr
                continue
            for x in row:
                word = findWholeWord('EST')(x)
                if word:
                    flag = True
            if flag:
                fobj.writerow(row)
            flag = False
            f.flush()

est_csv.close()

print total_rows

##file_name = 'Real_estatesdatan12345.csv'
##nf = base_dir+'filterdata.csv'
##nf = open(nf,'wb')
##nf = csv.writer(nf,delimiter=',')
##with open(base_dir+file_name,'rb') as myf:
##    lines = csv.reader(myf)
##    for c,line in enumerate(lines):
##        if not "REAL EST" in line[6]:            
##            nf.writerow(line)
##        else:
##            print c


            

             
