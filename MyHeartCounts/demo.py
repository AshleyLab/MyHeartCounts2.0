
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
#MHC.loadStudy(studyName = 'mindset_illness',studyTable = ' syn18143712', silent = False)
#MHC.loadStudy(studyName = 'mindset_adequacy',studyTable = ' syn18143711', silent = False)
#MHC.loadStudy(studyName = 'mindset_exercise',studyTable = ' syn18143709', silent = False)
#MHC.loadStudy(studyName = 'AB_TestResults',studyTable = 'syn7188351', silent = False)
select_healthCodes = MHC.UniqueUsers
select_healtHCodes = list(select_healthCodes)[1:5]
MHC.loadStudy(studyName = 'HealthKitDataCollector',studyTable = 'syn3560085', healthCodes = select_healthCodes, silent = True, limit = 100000)


print('retrieving blobs')
MHC.Studies[0].retrieve_blobs(select_healtHCodes,blob_names = ['data.csv'],silent=False)




#get daily step counts
#Stdy = MHC.stuides[0]
#user_to_dailyStepCounts = defaultdict(lambda: datatime)
#for user in MHC.Users:
    #for row in Stdy.observations:
        #if row['healthCode'] = user.healthCode:


print('complete')