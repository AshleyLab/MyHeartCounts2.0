
##############################
# author: Ali Javed
# October 3 Febuary 2022
# Description: Scripts demonstrates how to use the MyHeartCounts Python package.
# email: ajaved@stanford.edu; alijaved@live.com
#############################



#import libraries
from MyHeartCounts import MyHeartCounts
##############################

#Initilize a MyHeartCounts object
MHC = MyHeartCounts(user_password_file_path = '../../synapseAccess.txt', synapseCachePath = '/Users/ajaved/Three/MHC_DataBase/code/synapseCache')

#Rev up your engine!!
MHC.start()
#load a study
MHC.loadStudy(studyName = 'HealthKitWorkoutCollector',studyTable = 'syn3560095')

