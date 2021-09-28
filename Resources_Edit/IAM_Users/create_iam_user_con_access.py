"""Create IAM User with console login and a policy"""

import boto3
import botocore

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. default
        2. prod

        : """))
    
    if choose_local_profile_name == 1:
        local_profile_name = 'default'
    elif choose_local_profile_name == 2:
        local_profile_name = 'prod.account'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name

def get_password():
    pass 
    #here we are going to import the function created previously


def get_policy_arn():
    pass
    #Work in progress

def run():
    local_profile_name = profile_account()
    
    #to get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
    
    #to get to IAM
    iam_console = aws_mgmt_con.resource('iam')
    iam_client = aws_mgmt_con.client(service_name = "iam")

    #Get Details on a specific user
    iam_user_entry = input("Write the username: ")

    password = get_password()
    policy_arn = get_policy_arn()

    #to create a user
    iam_client.create_user(UserName = iam_user_entry)

    #provide console access
    iam_client.create_login_profile(UserName=iam_user_entry, Password=password, PasswordResetRequired=True)

    #attach policy
    iam_client.attach_user_policy(UserName=iam_user_entry, PolicyArn=policy_arn)



if __name__ == '__main__':
    run()