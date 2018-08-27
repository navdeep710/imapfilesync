#convert file from xlsx to csv
def convertxlsxtocsv(filename):
    pass

import xlrd
import csv

def replacefilenameext(filename,sheetname,origext=".xlsx",newext=".csv"):
    filename = filename.replace(origext,"")
    filename = filename + "_" + sheetname ;
    filename =  filename + newext
    return filename

def encodeifstring(value):
    if(isinstance(value,str)):
        return value.encode('ascii', 'ignore').decode('ascii')
    else:
        return value

def csv_from_excel(filename):
    print("converting {0} filename to csv".format(filename))
    wb = xlrd.open_workbook(filename)
    msheets = wb.sheet_names()
    newfilenames = []
    for sheet in msheets:
        sh = wb.sheet_by_name(sheet)
        if(sh.nrows > 0 ):
            sheetname = replacefilenameext(filename,sheet)
            new_csv = open(sheetname, 'w')
            wr = csv.writer(new_csv, quoting=csv.QUOTE_MINIMAL)
            for rownum in range(sh.nrows):
                wr.writerow([encodeifstring(s) for s in sh.row_values(rownum)])
            newfilenames.append(sheetname)
            new_csv.close()
    return newfilenames
