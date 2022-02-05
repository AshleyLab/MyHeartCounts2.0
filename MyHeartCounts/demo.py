
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
#Normally we set all the parameters of the script here, but for this presentation tutorial the values are at the location they are used. 
#all parameters set
##############################



#Initilize a MyHeartCounts object
MHC = MyHeartCounts(synapseUsername, synapsePassword, synapseCachePath = '/Users/ajaved/Three/MHC_DataBase/code/synapseCache')
#retrieve users from demographics tables of synapse#this line is not needed.
MHC.start()
#load a study
MHC.loadStudy(studyName = 'HealthKitWorkoutCollector',studyTable = 'syn3560095')



#calculate time
end= time.time()
difference = int(end - start)
print('Complete. '+str(difference))