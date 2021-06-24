"""This script will return a list of iam groups and its corresponding users
and store the information on a csv file - can be use for audit or gathering information"""

import boto3
import csv
import datetime

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. profile_1
        2. profile_2
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_profile_name == 1:
        local_profile_name = 'profile_1'
    elif choose_local_profile_name == 2:
        local_profile_name = 'profile_2'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name


def run():
    local_profile_name = profile_account()
    
    #Get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
    
    #Get cloudwatch client conection
    iam_con_cli = aws_mgmt_con.client(service_name='iam')
    response_groups = iam_con_cli.list_groups(MaxItems=200)
    
    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_iam_policy-grp_inv.csv'

    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['GroupName','PolicyName'])  
    
    for iam_group in response_groups['Groups']:
       iam_group_name = iam_group['GroupName']
       response_policies = iam_con_cli.list_attached_group_policies(GroupName=iam_group_name)
       
       if not response_policies['AttachedPolicies']:
           csv_write_object.writerow([iam_group_name, 'Group with no policy'])
       else:
            for policy in response_policies['AttachedPolicies']:
                iam_policy = policy['PolicyName']
                csv_write_object.writerow([iam_group_name, iam_policy])
        
    csv_object.close()

if __name__ == '__main__':
    run()