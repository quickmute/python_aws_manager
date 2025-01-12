# package aws/aws.py
import boto3
## This is the parent of all AWS related classes, use this as a starting point
## This will set the session for you
## You have to define getters and setters in order for the children to be able to see your private attributes, or you can just expose them 
##  Double underline makes it private in scope
## If you are in local, pass in profile
## If you are inside Lambda, pass in botocore_session = boto3.Session()
## If you are doing sts assumeRole inside Lambda to another role, then pass in access_key_id
class aws:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, region_name="us-east-1", botocore_session=None, profile_name=None):
        if (botocore_session):
            self.__mySession = botocore_session
        elif (profile_name):
            self.__mySession = boto3.Session(
                profile_name=profile_name, 
                region_name=region_name
            )
        elif (aws_access_key_id and aws_secret_access_key and aws_session_token):
            self.__mySession = boto3.Session(
                aws_access_key_id=aws_access_key_id, 
                aws_secret_access_key=aws_secret_access_key, 
                aws_session_token=aws_session_token, 
                region_name=region_name
            )
        else:
            self.__mySession = None
            print("No session created")
            return False
        
        self.__region = region_name
    
    def get_session(self):
        return self.__mySession
    def get_region(self):
        return self.__region
    def show_region(self):
        print(self.__region)
    def show_resource(self):
        ## Override this in children class
        pass