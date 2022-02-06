#python libraries needed in code

class Study:
    def __init__(self, studyName,studyTable):
        ##############################
        # author: Ali Javed
        # October: 3 February 2022
        # email: ajaved@stanford.edu; alijaved@live.com
        #############################
        # Description:Class initilizer for a study. Model assumes that study will be in a single table.
        
        # Inputs
        #StudyName: Study name for readability
        #TableName: Table name in synapse.
        #Output
        #Study Object
    
        ########################################
        
        #check if synapse connection is active (I am not sure if there is a timeout). If not activate it again.
        self.studyName = studyName
        self.studyTable = studyTable


        #study data. These are essentially rows in table. Parsed if you have a parser.
        self.observations = []

        #Users enrolled in study.
        self.studyUsers = set()


    def parse_observation(self, observation):
        #############################
        # Description: Parse a single observation in a study. This is a dataframe row. This function, is a wrapper that calls appropriate parsing function.

        # Inputs:
        # observation: Row of dataframe in study table
        # Output:
        # observation: Parsed/cleaned row of dataframe provided as input

        ########################################
        #add do before study name to match the parsing function name. We do not want to expose all the functions to external use. Chosing studyName instead of table because
        #two studies/tables can have same parsing, such a V1 and V2
        parser_function_name = f"do_{self.studyName}"


        #some libraries used in below line
        #The hasattr() method returns true if an object has the given named attribute and false if it does not.
        #In general, a callable is something that can be called. This built-in method in Python checks and returns True if the object passed appears to be callable, but may not be, otherwise False.
        #The getattr() method returns the value of the named attribute of an object. If not found, it returns the default value provided to the function.

        #check if we have a function for parsing, if so parse and return observation
        if hasattr(self, parser_function_name) and callable(func := getattr(self, parser_function_name)):
            observation = func(observation)
            return observation

        #if there is no parser, just return observation as is.
        else:
            return observation






    def do_HealthKitWorkoutCollector(self,observation):
        #############################
        # Description: Row parsing for the HealthKitWorkoutCollector table
        # contributed by other team members.

        # Inputs:
        # row: row object to be parsed. This is a row from the dataframe loaded from synapse.
        # Output:
        # row

        ########################################

        #just return what is recieved.
        return observation


    def add_observation(self,observation):
        self.observations.append(observation)

        return True

    def parse_all_observations(self):
        #############################
        # Description: Function parses all data stored in observations if parser is available


        # Inputs:
        # None. Function uses self.observations
        # Output:
        # None. Function updates self.observations

        ########################################

        #loop through all observations in self.observations and update them to parsed version if parser is available for current studyName.
        for i in range(0,len(self.observations)):
            self.observations[i]= self.parse_observation(self.observations[i])

        return True

    def refresh_studyUsers(self):
        #############################
        # Description: Function refreshes the list of study users. Usefull to know which users are in the study

        # Inputs:
        # None. Function uses self
        # Output:
        # None. Function updates self

        ########################################

        self.studyUsers = set()
        for observation in self.observations:
            #each observation must have a healthCode
            self.studyUsers.add(observation['healthCode'])


        return True










        
        
        
        
 
