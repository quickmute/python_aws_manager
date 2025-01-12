# package aws/iam_user.py
import boto3
import botocore
from datetime import datetime, timezone

from . aws import aws
from . aws_support import parse_tags

class iam_user(aws):
    def __init__(self, username, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, region_name="us-east-1", botocore_session=None, profile_name=None):
        super().__init__(
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key, 
            aws_session_token=aws_session_token, 
            region_name=region_name, 
            botocore_session=botocore_session, 
            profile_name=profile_name
        )
        self.__client = self.get_session().client('iam', region_name=self.get_region())        
        self.__username = username

        self.__user = self.__get_user()
        if (self.__user == False):
            raise Exception("Unable to get user")
            return False
        
        self.__userTags = self.__get_tags()
        self.__userAccessKeys = self.__get_access_key()
        
    def __get_user(self):
        ## Simple call to get user with try except
        try:
            user = self.__client.get_user(UserName=self.__username)
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
        except self.__client.exceptions.NoSuchEntityException:
            print("No Such User Exists")
            return False
        except self.__client.exceptions.ServiceFailureException as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False
        return user.get('User')

    def __get_tags(self):
        ## Simple call to get tags of user with try except and parsed to dictionary
        try:
            tags = self.__client.list_user_tags(UserName=self.__username)
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
        except self.__client.exceptions.NoSuchEntityException:
            ## No tags
            return {}
        except self.__client.exceptions.ServiceFailureException as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False
        return parse_tags(tags.get('Tags'))

    def __get_access_key(self):
        ## call to get all access key of User, last used, and age of created and used in days
        try:
            userAccessKeys = self.__client.list_access_keys(UserName=self.__username).get('AccessKeyMetadata')
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
        except self.__client.exceptions.NoSuchEntityException:
            ## No access keys
            return []
        except self.__client.exceptions.ServiceFailureException as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False
        
        now = datetime.now(timezone.utc)
        for accessKey in userAccessKeys:
            accessKey['LastUsed'] = None
            try:
                response = self.__client.get_access_key_last_used(AccessKeyId=accessKey["AccessKeyId"])
            except botocore.exceptions.ClientError as e:
                print(e)
                return False
            except Exception as e:
                print(e)
                return False
            accessKey['LastUsed'] = response.get('AccessKeyLastUsed',{}).get('LastUsedDate',None)
            accessKey['CreatedAgeDays'] = (now - accessKey["CreateDate"]).days if accessKey["CreateDate"] != None else 0
            accessKey['UsedAgeDays'] = (now - accessKey["LastUsed"]).days if accessKey["LastUsed"] != None else 0
            
        return userAccessKeys

    def show_resources(self):
        print(self.get_user())
        print(self.get_user_tags())
        print(self.get_user_access_keys())
    
    def get_user_tags(self):
        return self.__userTags

    def get_user_access_keys(self):
        return self.__userAccessKeys

    def get_user(self):
        return self.__user
    
    def delete_access_key(self, access_key_id):
        try:
            self.__client.delete_access_key(UserName=self.get_user().UserName, AccessKeyId=access_key_id)
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
        return True
