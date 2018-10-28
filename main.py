import pandas as pd
import csv,buildinginfo, re
import globalparameter
from collections import Counter, OrderedDict

def CountAttributes(filename):
    with open(filename,'r') as f:
        reader = csv.DictReader(f)
        counters = OrderedDict((attr,Counter()) for attr in reader.fieldnames)
        for row in reader:
            for attr, value in row.items():
                counters[attr][value] += 1
    return counters

def ReadYears(filename):
    buildingid_list = []
    year_list = []
    with open(filename,'r') as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            buildingid_list.append(row[0])
            regex_date = re.compile('[0-9]{4}')
            if regex_date.findall(row[7]) == []:
                year_list.append(0)
            else:
                year = regex_date.findall(row[7])
                year_list.append(int(year[0]))


    df = pd.DataFrame({'BUILDING_ID':buildingid_list,'buildyear':year_list})
    df.to_csv(globalparameter.GlobalFilePath+'/buildyear.csv',index=False)

if __name__ == '__main__':

    # statistic of buildings.csv

    # testdatafile = globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0]
    # for attr,counts in CountAttributes(testdatafile).items():
    #     print('{}: {}'.format(attr, dict(counts)))
    # print(1)

    datafile = globalparameter.GlobalFilePath+'/output.csv'
    ReadYears(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0])
    counterattributess =  CountAttributes(datafile)
    iterator=0
    build_unit_id_list = []
    build_unit_num_list = []

    build_attr_name = ''
    for attr, counter in counterattributess.items():
        iterator = iterator + 1
        if iterator==2:
            build_attr_name = attr
            dictionarycount = dict(counter)
            for name1,value1 in dictionarycount.items():
                build_unit_id_list.append(name1)
                build_unit_num_list.append(value1)
        # print('{}: {}'.format(attr, dict(counts)))
    df = pd.DataFrame({build_attr_name:build_unit_id_list, 'unit_num':build_unit_num_list})
    df.to_csv(globalparameter.GlobalFilePath+'/unitnum.csv',index=False)

    csv_buildings = pd.read_csv(globalparameter.GlobalFilePath + '/' + globalparameter.CSVFileNames[0])
    csv_building_years = pd.read_csv(globalparameter.GlobalFilePath + '/buildyear.csv')
    csv_unit_num = pd.read_csv(globalparameter.GlobalFilePath+'/unitnum.csv')
    merged_1 = csv_buildings.merge(csv_building_years,on='BUILDING_ID')
    merged_2 = csv_unit_num.merge(merged_1, on='BUILDING_ID')
    merged_2.to_csv(globalparameter.GlobalFilePath+"/building_update.csv", index=False)
