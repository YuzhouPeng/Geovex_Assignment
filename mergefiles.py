import globalparameter
import pandas as pd



csv_buildings = pd.read_csv(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[0])
csv_coords = pd.read_csv(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[1])
csv_schools = pd.read_csv(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[2])
csv_units = pd.read_csv(globalparameter.GlobalFilePath+'/'+globalparameter.CSVFileNames[3])

merged1 = csv_buildings.merge(csv_coords, on='BUILDING_ID')
merged2 = csv_units.merge(merged1,on='BUILDING_ID')
merged2.to_csv(globalparameter.GlobalFilePath+"/output.csv", index=False)

