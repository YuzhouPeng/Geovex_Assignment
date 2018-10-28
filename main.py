import pandas as pd
import csv,buildinginfo, re, geopy.distance
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

def CalculateDistance(latitude1, longitude1, latitude2, longitude2):
    coord1 = (latitude1,longitude1)
    coord2 = (latitude2,longitude2)
    distance = geopy.distance.distance(coord1,coord2).km
    # print(distance)
    return distance

def FindSuitableBuilding():
    return

if __name__ == '__main__':

    # Statistic of buildings.csv

    # testdatafile = globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0]
    # for attr,counts in CountAttributes(testdatafile).items():
    #     print('{}: {}'.format(attr, dict(counts)))
    # print(1)

    # Find suitable buildings

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

    with open(globalparameter.GlobalFilePath+'/building_update.csv','r') as f:
        reader = csv.reader(f)
        next(f)
        max_unit_num = 0
        max_unit_num_id = 0
        for row in reader:
            if int(row[1])>int(max_unit_num) and int(row[11]) > 1980:
                max_unit_num = row[1]
                max_unit_num_id = row[0]

        print('id of the building id is: {}'.format(max_unit_num_id))

    # id:1401193775 coord: LAT:53.342715 LON:-6.236459

    # Calculate distance
    school_id = []
    school_latitude = []
    school_longitude = []
    school_type = []
    with open(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[2],'r') as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            school_id.append(int(row[0]))
            school_latitude.append(float(row[1]))
            school_longitude.append(float(row[2]))
            if row[3] =='POST-PRIMARY':
                school_type.append(1)
            elif row[3] == 'PRIMARY':
                school_type.append(2)
            else:
                school_type.append(-1)
    mindistance = 9999
    mindistance_schoolid = 0
    postprimary_number = 0
    for i in range(267):
        school_building_distance = CalculateDistance(53.342715,-6.236459,school_latitude[i],school_longitude[i])
        if school_building_distance<mindistance:
            mindistance = school_building_distance
            # print(mindistance)
            mindistance_schoolid = school_id[i]
        # if school_type[i]==1:
        #     print('post-primary distance: {}'.format(school_building_distance))
        if school_building_distance<3 and school_type[i]==1:
            postprimary_number = postprimary_number+1



    print('building id of shortest distance of school and building is {} and the distance is: {}'.format(mindistance_schoolid,mindistance))
    print('number of post-primary school within 3 km is {}'.format(postprimary_number))
