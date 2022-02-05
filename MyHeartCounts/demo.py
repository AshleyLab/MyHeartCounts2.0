
#import libraries
from MyHeartCounts import MyHeartCounts
import warnings
import time

##############################
# author: Ali Javed
# October 3 Febuary 2022
# email: ajaved@stanford.edu; alijaved@live.com
#############################

#start timer
start = time.time()

        
warnings.filterwarnings("ignore")

#Path to Username Password file. Replace the path with path to the file that has your synapse credentials. Put the username in first line and password in second.
f=open("../../synapseAccess.txt","r")
lines=f.readlines()
synapseUsername=lines[0].strip()
synapsePassword=lines[1].strip()
f.close()

#Synapse Cache path
#this is where my synapseCache is. Set cache path or leave empty for default value

MHC = MyHeartCounts(synapseUsername, synapsePassword, synapseCachePath = '/Users/ajaved/Three/MHC_DataBase/code/synapseCache')


#retrieve users from demographics tables of synapse
MHC.retrieveAllUsers()
MHC.loadStudy(studyName = 'HealthKitWorkoutCollector',studyTable = 'syn3560095')




#get list of users
#users = MHC.get_users()

#get studies
studies = MHC.get_studies()

#calculate time
end= time.time()
difference = int(end - start)



print('Data retrival, loading, cleaning and parsing complete in '+str(difference)+' seconds.')