import csv

file = 'outputdatafinal_2.csv'
with open(file, 'rb') as mf:
    reader = csv.reader(mf, delimiter=",")
    wf = open('outputdatafinal.csv', 'wb')
    writer = csv.writer(wf)
    cols = reader.next()
    writer.writerow(cols)
    for ctr,row in enumerate(list(reader)):
##        row = list(reader)[ctr]
        city_state_zip = row[8]
        city_state_zip = city_state_zip.split(',')
        print ctr
        if city_state_zip:
            city = city_state_zip[0]
            row[-3] = city
            print city
            try:            
                state_zip = city_state_zip[1]
                if state_zip:
                    state_zip = state_zip.split()
                    if state_zip:
                        print state_zip
                        state = state_zip[0]
                        row[-2] = state
                        zipcode = state_zip[-1]
                        row[-1] = '%s' % str(zipcode)
            except Exception as e:
                pass
                        
        zipcode = row[-6]
        if not zipcode.strip():
            writer.writerow(row)
            continue
        zipcode = "0%s" % zipcode
        row[-6] = zipcode
        writer.writerow(row)
        print zipcode        
