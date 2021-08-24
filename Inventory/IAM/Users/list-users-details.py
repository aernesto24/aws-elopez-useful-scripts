"""This script will return deatails of an specific user"""

import boto3
import botocore

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. <local_profile 1 on .aws/config>
        2. <local_profile 2 on .aws/config>
        3. <local_profile 3 on .aws/config>
        : """))
    
    if choose_local_profile_name == 1:
        local_profile_name = '<local_profile 1 on .aws/config>'
    elif choose_local_profile_name == 2:
        local_profile_name = '<local_profile 2 on .aws/config>'
    elif choose_local_profile_name == 3:
        local_profile_name = '<local_profile 3 on .aws/config>'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name


def run():
    local_profile_name = profile_account()
    
    #to get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
    
    #to get to IAM
    iam_console = aws_mgmt_con.resource('iam')

    #Get Details on a specific user
    iam_user_entry = input("Write the username: ")

    #Print user details
    #print(dir(iam_user_object))
    try:
        print("Details for IAM users: " + iam_user_entry)
        iam_user_object = iam_console.User( iam_user_entry )

        #obtain information about user with mfa
        if iam_user_object.mfa_devices:
            mfa_enabled = True
        else:
            mfa_enabled = False
        
        #Print the user information
        print("Username: " + iam_user_object.user_name + "\n" +
                "UserID: " + iam_user_object.user_id + "\n" +
                "password last used:" + iam_user_object.password_last_used.strftime("%Y-%m-%d") + "\n" +
                "And is MFA Enabled?: " + str(mfa_enabled) + "\n")
    
    except iam_console.meta.client.exceptions.NoSuchEntityException:
        print("User " + iam_user_entry + " does not exist!")

if __name__ == '__main__':
    run()