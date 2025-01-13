# package aws/main.py
import sys, getopt
from aws.aws import aws
from aws.iam_user import iam_user

def usage():
    print('Usage: ' + sys.argv[0] + ' --username <username> --profile <profile> --region <region>')

def main(argv):
    username = None
    profile = None
    region = None
    try:
        opts, args = getopt.getopt(argv,"hu:p:r:",["username=","profile=","region="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--profile"):
            profile = arg
        elif opt in ("-r", "--region"):
            region = arg
    if (username == None):
        usage()
        sys.exit(2)
    if (profile == None):
        profile = "default"
    if (region == None):
        region = "us-east-1"
    
    user = iam_user(username=username, profile_name=profile, region_name=region)
    user.show_resources()

if __name__ == "__main__":
    main(sys.argv[1:])