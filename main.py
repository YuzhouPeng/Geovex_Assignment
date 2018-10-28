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
    with open(filename,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[7]!= None:
                regex_year = re.compile('[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{4}')

if __name__ == '__main__':

    # statistic of buildings.csv

    # testdatafile = globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0]
    # for attr,counts in CountAttributes(testdatafile).items():
    #     print('{}: {}'.format(attr, dict(counts)))
    # print(1)

    datafile = globalparameter.GlobalFilePath+'/output.csv'
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
    df.to_csv(globalparameter.GlobalFilePath+'/unitnum.csv')

    csv_buildings = pd.read_csv(globalparameter.GlobalFilePath + '/' + globalparameter.CSVFileNames[0])
    merged_new_building =
