import pandas as pd
import csv,buildinginfo, re, geopy.distance
import globalparameter
from collections import Counter, OrderedDict


def MergeFiles():
    csv_buildings = pd.read_csv(globalparameter.GlobalFilePath + '/' + globalparameter.CSVFileNames[0])
    csv_coords = pd.read_csv(globalparameter.GlobalFilePath + '/' + globalparameter.CSVFileNames[1])
    csv_schools = pd.read_csv(globalparameter.GlobalFilePath + '/' + globalparameter.CSVFileNames[2])
    csv_units = pd.read_csv(globalparameter.GlobalFilePath + '/' + globalparameter.CSVFileNames[3])

    merged1 = csv_buildings.merge(csv_coords, on='BUILDING_ID')
    merged2 = csv_units.merge(merged1, on='BUILDING_ID')
    merged2.to_csv(globalparameter.GlobalFilePath + "/output.csv", index=False)


def CountAttributes(filename):
    with open(filename,'r') as f:
        reader = csv.DictReader(f)
        counters = OrderedDict((attr,Counter()) for attr in reader.fieldnames)
        for row in reader:
            for attr, value in row.items():
                counters[attr][value] += 1
    return counters

def flatten(nestlist):
    for i in nestlist:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

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

def FindSchoolDistance(buildingid):
    # Find latitude and longitude of building
    building_latitude = 0
    building_longitude = 0
    with open(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[1],'r') as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            if buildingid==int(row[0]):
                building_latitude = float(row[1])
                building_longitude = float(row[2])
    # Calculate school distance
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
        school_building_distance = CalculateDistance(building_latitude,building_longitude,school_latitude[i],school_longitude[i])
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


def FindSuitableBuilding(datafile):

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
    return int(max_unit_num_id)


def CalculatePopulation(filename,selected_columns):
    totalpop = 0
    for i in range(len(selected_columns)):
        with open(filename) as f:
            next(f)
            totalpop = totalpop+ sum(int(r[selected_columns[i]]) for r in csv.reader(f))
    return totalpop

def CalculateSmallArea():
    # columns = list(range(15,30))+list(range(50,65))
    columns = list(range(85,100))
    totalpopulation = CalculatePopulation(globalparameter.GlobalFilePath+'/SAPS2016_SA2017.csv',columns)
    print('population of people between 12-54 is {}'.format(totalpopulation))
if __name__ == '__main__':

    # Data preparation
    MergeFiles()

    # Statistic of buildings.csv

    # testdatafile = globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0]
    # for attr,counts in CountAttributes(testdatafile).items():
    #     print('{}: {}'.format(attr, dict(counts)))
    # print(1)


    # Assignment 1

    datafile = globalparameter.GlobalFilePath+'/output.csv'
    # Convert date using regular expression
    ReadYears(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0])
    # Find the building that meet requirements
    buildingid = FindSuitableBuilding(datafile)
    # id:1401193775 coord: LAT:53.342715 LON:-6.236459
    # Calculate distance between
    FindSchoolDistance(buildingid)
    # Bonus question
    CalculateSmallArea()

    # Assignment 2

    test = [[1, 2, [3]], 4]
    print(list(flatten(test)))


