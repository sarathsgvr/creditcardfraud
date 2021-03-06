import os
from datetime import datetime
import json
import shutil
import pandas as pd
import re
from application_logging import logger

class Raw_Data_Validation:
    def __init__(self, path):
        self.Directory = path
        self.schema_path = 'schema_training.json'
        self.logger = logger.App_Logger()

    def values_from_schema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthofDateStampinFile = dic['LengthofDateStampinFile']
            LengthofTimeStampinFile = dic['LengthofTimeStampinFile']
            column_name = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

            file = open("TrainingLogs/SchemaValidationlog.txt", 'a+')
            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberofColumns + "\n"
            self.logger.log(file, message)
            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

    def Regex_Creation(self):
        regex = "['creditcardfraud']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryForGoodBadRawData(self):
        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as ex:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):
        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path+'Good_Raw'):
                shutil.rmtree(path+'Good_Raw')
                file = open(Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file,"GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as o:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %o)
            file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):
        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path+'Bad_Raw'):
                shutil.rmtree(path+'Bad_Raw')
                file = open(Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file,"BadRaw directory deleted successfully!!!")
                file.close()
        except OSError as o:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %o)
            file.close()
            raise OSError
    
    def validatefilename(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        self.deleteExistingGoodDataTrainingFolder()
        self.deleteExistingBadDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()
        filelist = [f for f in os.listdir(self.Directory)]
        try:
            f = open("Training_Logs/namevalidationlog.txt", 'a+')
            for filename in filelist:
                if (re.match(regex, filename)):
                    splitatdot = re.split('.csv', filename)
                    splitatdot = re.split('_', splitatdot[0])
                    if len(splitatdot[1]) == LengthOfDateStampInFile:
                        if len(splitatdot[2]) == LengthOfTimeStampInFile:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Good_Raw")
                            self.logger.log(f,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)
                        else:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                            self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                        self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                    self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
            f.close()
        
        except Exception as e:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error while validating filename %s" %e)
            f.close()
            raise e
    
    def validatecolumns(self, NumberofColumns):
        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Columns length validation started!")
            for file in os.listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                if csv.shape[1] == NumberofColumns:
                    pass
                else:
                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/Bad_Raw")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(f, "Column Length Validation Completed!!")

        except OSError:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Column validation failed! %s" % OSError)
            f.close()
            raise OSError

    def validatemissingvalues(self):
        try:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log("Missing value validation started!")
            for file in os.listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv('Training_Raw_files_validated/Good_Raw/'+file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file,
                                    "Training_Raw_files_validated/Bad_Raw")
                        self.logger.log(f,"Invalid Column for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=None, header=True)
        except OSError:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()


                        

    

        