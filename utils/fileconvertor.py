#convert file from xlsx to csv
def convertxlsxtocsv(filename):
    pass

import xlrd
import unicodecsv as csv

def replacefilenameext(filename,sheetname,origext=".xlsx",newext=".csv"):
    filename = filename.replace(origext,"")
    filename = filename + "_" + sheetname ;
    filename =  filename + newext
    return filename

def encodeifstring(value):
    if isinstance(value, str):
        return value.encode('utf-8')
    else:
        return str(value)

def csv_from_excel(filename):
    print("converting {0} filename to csv".format(filename))
    wb = xlrd.open_workbook(filename)
    msheets = wb.sheet_names()
    newfilenames = []
    for sheet in msheets:
        sh = wb.sheet_by_name(sheet)
        if sh.nrows > 0:
            sheetname = replacefilenameext(filename,sheet)
            new_csv = open(sheetname, 'wb')
            wr = csv.writer(new_csv)
            for rownum in range(sh.nrows):
                temp = [s for s in sh.row_values(rownum)]
                wr.writerow(temp)
            newfilenames.append(sheetname)
            new_csv.close()
    return newfilenames

