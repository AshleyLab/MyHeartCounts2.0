
##############################
# author: Ali Javed
# October 3 Febuary 2022
# Description: Scripts demonstrates how to use the MyHeartCounts Python package.
# email: ajaved@stanford.edu; alijaved@live.com
#############################



#import libraries
from MyHeartCounts import MyHeartCounts
import warnings
import time
warnings.filterwarnings("ignore")
#start timer
start = time.time()



        

##############################
#set parameters
#Path to Username Password file. Replace the path with path to the file that has your synapse credentials. Put the username in first line and password in second.
f=open("../../synapseAccess.txt","r")
lines=f.readlines()
synapseUsername=lines[0].strip()
synapsePassword=lines[1].strip()
f.close()

#Synapse Cache path. Set cache path or leave empty for default value
synapseCachePath = '/Users/ajaved/Three/MHC_DataBase/code/synapseCache'

#Load a study. Name the study (usually table name), and study table to retrieve data from synapse.
studyName = 'HealthKitWorkoutCollector'
studyTable = 'syn3560095'
#all parameters set
##############################



#Initilize a MyHeartCounts object
MHC = MyHeartCounts(synapseUsername, synapsePassword, synapseCachePath = synapseCachePath )
#retrieve users from demographics tables of synapse
MHC.retrieveAllUsers()
MHC.loadStudy(studyName,studyTable)

#get list of users
#users = MHC.get_users()

#get studies
#studies = MHC.get_studies()

#calculate time
end= time.time()
difference = int(end - start)
print('Data retrival, loading, cleaning and parsing complete in '+str(difference)+' seconds.')