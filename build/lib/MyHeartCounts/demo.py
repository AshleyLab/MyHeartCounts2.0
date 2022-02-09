
##############################
# author: Ali Javed
# October 3 Febuary 2022
# Description: Scripts demonstrates how to use the MyHeartCounts Python package.
# email: ajaved@stanford.edu; alijaved@live.com
#############################



#import libraries
#from myHeartCounts.MyHeartCounts import MyHeartCounts
from myHeartCounts import MyHeartCounts
from datetime import datetime
##############################

#Initilize a MyHeartCounts object
MHC = MyHeartCounts(user_password_file_path = '../../synapseAccess.txt',synapseCachePath ='/Users/ajaved/Three/MHC_DataBase/code/synapseCache')

#Rev up your engine!!
MHC.start()
#load a study
#MHC.loadStudy(studyName = 'mindset_illness',studyTable = ' syn18143712')
#MHC.loadStudy(studyName = 'mindset_adequacy',studyTable = ' syn18143711')
#MHC.loadStudy(studyName = 'mindset_exercise',studyTable = ' syn18143709')
MHC.loadStudy(studyName = 'AB_TestResults',studyTable = 'syn7188351')
#only download data for users we have in coacing study

select_healthCodes = sorted(MHC.Studies[0].studyUsers)
select_healthCodes = list(select_healthCodes)[1:5]
MHC.loadStudy(studyName = 'HealthKitDataCollector',studyTable = 'syn3560085', healthCodes = [], silent = True,limit = 10)


#print('retrieving blobs')
MHC.Studies[1].retrieve_blobs(blob_names = ['data.csv'],healthCodes = [], silent=False)



print('complete')