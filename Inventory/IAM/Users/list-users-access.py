"""This script will return a list of users and password last used"""

import boto3

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
    
    for user in iam_console.users.all():
        print(user.name, '  ',  user.password_last_used)

if __name__ == '__main__':
    run()