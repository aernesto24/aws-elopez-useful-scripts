"""This script will return a list of iam groups and its corresponding users
and store the information on a csv file - can be use for audit or gathering information"""

import boto3
import csv
import datetime

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. goku
        2. default
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_profile_name == 1:
        local_profile_name = 'goku'
    elif choose_local_profile_name == 2:
        local_profile_name = 'default'
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
    response_groups = iam_con_cli.list_groups(MaxItems=105)
    
    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_iam_grp-usr_inv.csv'

    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['GroupName','Username'])  
    
    #interate through the groups and users 
    for iam_group in response_groups['Groups']:
        #print(iam_group['GroupName'])
        iam_group_name = iam_group['GroupName']
        response_users_in_group = iam_con_cli.get_group(GroupName=iam_group_name)
        
        if not response_users_in_group['Users']:
            csv_write_object.writerow([iam_group_name, 'Empty group'])
        else:
            for each_user in response_users_in_group['Users']:
                iam_username = each_user['UserName']
    
                # print(iam_group_name, ' ', each_user['UserName'])
                #write the groupName and username
                csv_write_object.writerow([iam_group_name, iam_username])
    
    csv_object.close()


if __name__ == '__main__':
    run()