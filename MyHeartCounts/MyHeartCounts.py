#python libraries needed in code
from User.User import User
from Study.Study import Study
import synapseclient
from datetime import datetime

class MyHeartCounts:
    def __init__(self, synapseUserName, synapsePassword,synapseCachePath = ''):
        ##############################
        # author: Ali Javed
        # October: 3 February 2022
        # email: ajaved@stanford.edu; alijaved@live.com
        #############################
        # Description: Class is used to access My Heart Counts data on Synapse and user interaction data on Amazon Web Services.
        
        # Inputs
        # SynapseUser: Username of Synapse Account
        # SynapsePassword: Password for Synapse Account
        
        #To access Amazon S3 a key needs to be set up. For instructions
        # Amazon Key: Figure out how to best set this
        
        #Output
        #An Object of MyHeartCounts
    
        ########################################
        
        #Declare Class variables
        
        #The My Heart Counts model has 3 sub objects.
        #User class is a class that has ittrebutes about a User. Attributes also incluce user interactions on the APP loaded through Amazon Web Services.
        self.Users = []

        #set of unique users
        self.UniqueUsers = set()

        #Study contains details of a particular study. Such as User, 6 min-walk test results, phone model used etc.
        self.Studies = []


        self.synapseCachePath = synapseCachePath
        self.synapseUserName = synapseUserName
        self.synapsePassword = synapsePassword
        self.synapseConection = None

    def refresh_UniqueUsers(self):

        #############################
        # Description: Functions refreshed list of unique users

        # Inputs:
        # None
        # Output:
        # None
        #############################################################################

        for user in self.Users:
            self.UniqueUsers.add(user.healthCode)

    def connectToSynapse(self, multi_threaded = True,silent=True):
        #############################
        # Description: Function connects to synapse, incase of longer analysis there may be a time out

        # Inputs:
        # multi_threaded: Synapse connection parameter
        # Output:
        # None
        #############################################################################
        # Synapse Connection
        # Read https://python-docs.synapse.org/build/html/index.html for details
        if self.synapseCachePath == '':
            synapseConnection = synapseclient.Synapse(silent = silent)
        else:
            synapseConnection = synapseclient.Synapse(cache_root_dir=self.synapseCachePath, silent = silent)
        synapseConnection.multi_threaded = multi_threaded
        
        #return the status of connection
        synapseConnection.login(self.synapseUserName, self.synapsePassword)
        return synapseConnection
        #############################################################################


    def start(self):
        #############################
        # Description: Function retrieves users from demographics tables V1 and V2 from synapse. Start seems like a user friendly way to say it.

        # Inputs:
        # None
        # Output:
        # None
        #############################################################################

        #connect to synapse
        self.synapseConnection = self.connectToSynapse()
        print('Retrieving user data. This may take some time if cache is empty.')
        
        #Data retrieval, parsing and clearning
        #There are two tables that have base data related to users, and not to MHC studies. We can add more tables here to be read.
        demographicsTables = ['syn3917840','syn21455306']
        #Only columns that do not require cleaning/ parsing
        
        #These are the columns we read
        #demographicsColumns = ['recordId','appVersion','phoneInfo','healthCode','createdOn','userSharingScope','studyMemberships']
        for table in demographicsTables:
            #Retrieve data in descending order on created on. This way for each user we save the first entry they made in case of duplicate entries.
            #The expectation is that the first entry is more likley to be correct in case of a disagreement in entries.
            query = "Select * from " + table + ' ORDER BY createdOn DESC'
            #Query synapse
            response = self.synapseConnection.tableQuery(query)
            #convert the response to a dataframe and load in our users object
            response_df = response.asDataFrame()
            # convert to dictioanry

            for index, row in response_df.iterrows():

                #parse and clean columns that require. If any value is missing set it to nan (not a number)
                createdOn = datetime.fromtimestamp(row['createdOn'] / 1e3)
                healthCode = row['healthCode']

                user_dict = {}
                user_dict['healthCode'] = healthCode
                user_dict['createdOn'] = createdOn
                try:
                    user_dict['daysInStudy'] = row['dayInStudy']
                except:
                    user_dict['daysInStudy'] = float('nan')

                try:
                    user_dict['weight'] = float(row['NonIdentifiableDemographics.patientWeightPounds'])
                except:
                    user_dict['weight'] = float('nan')

                try:
                    user_dict['gender'] = str(row['NonIdentifiableDemographics.patientBiologicalSex']).lower()
                except:
                    user_dict['gender'] = 'Unknown'

                try:
                    user_dict['bloodType'] = str(row['NonIdentifiableDemographics.patientBloodType'])
                except:
                    user_dict['bloodType'] = 'Unknown'

                try:
                    user_dict['skinType'] = str(row['NonIdentifiableDemographics.patientFitzpatrickSkinType'])
                except:
                    user_dict['skinType'] = 'Unknown'

                try:
                    user_dict['height'] = float(row['NonIdentifiableDemographics.patientHeightInches'])
                except:
                    user_dict['height'] = float('nan')

                #for date of birth we need to minus age from createdOn date
                try:
                    user_dict['dob'] = createdOn- datetime.timedelta(years = float(row['NonIdentifiableDemographics.patientCurrentAge']))
                except:
                    #setting a date time object allows error free parsing, however we set it to 1800 so it is obviously incorrect
                    user_dict['dob'] = datetime(1800, 10, 5, 18, 0)

                #initilize a user object
                user_obj = User(healthCode)
                #set user attributes
                user_obj.set_attributes(user_dict)

                #add the user object to our list of users in MHC
                self.Users.append(user_obj)

            #############################################################################

        #update set of users in MHC.
        self.refresh_UniqueUsers()

        #logout of synapse once done.
        status = self.synapseConnection.logout()
        
        if status != None:
            print('Logout not sucessfull')
        #Data loading and class initilization complete.




    def get_users(self):
        #############################
        # Description: Class is used to access My Heart Counts data on Synapse and user interaction data on Amazon Web Services.

        # Inputs:
        #None
        # Output:
        # self.Users: List of user objects that contain all the loaded users.

        ########################################
        return self.Users

        
    def loadStudy(self,studyName, studyTable, studyObservationParseFunction = None ):
        #############################
        # Description: Class loads study, if parser is available, parses data, otherwise users can pass a parsing function for their study, or user existing parsers for the particular study
        # contributed by other team members.

        # Inputs:
        # None
        # Output:
        # self.Users: List of user objects that contain all the loaded users.

        ########################################

        # connect to synapse
        self.synapseConnection = self.connectToSynapse()
        print('Retrieving study data. This may take some time if cache is empty.')

        #get all data from the study table
        query = "Select * from " + studyTable + ' ORDER BY createdOn DESC'
        response = self.synapseConnection.tableQuery(query)
        
        

        # convert the response to a dataframe and load in our users object
        response_df = response.asDataFrame()
        
        #retrieve file paths here.

        # logout of synapse once done.
        studyObj = Study(studyName, studyTable)

        #iterate of data to parse, clean and store
        for index, observation in response_df.iterrows():
            observation = studyObj.parse_observation(observation)
            studyObj.add_observation(observation)


        #update set of users enrolled in study.
        studyObj.refresh_studyUsers()

        #add study to list of studies
        self.Studies.append(studyObj)


        #logout of synapse
        status = self.synapseConnection.logout()
        if status != None:
            print('Logout not sucessfull')
        # Data loading and class initilization complete.
        
        
        return True


    def get_studies(self):

        #############################
        # Description: Retuens loaded studies
    
        # Inputs:
        # None. Function uses self
        # Output:
        # None. Function updates self
    
        ########################################
        
        return self.Studies
        



            


        
        
        
        
        
        
 
