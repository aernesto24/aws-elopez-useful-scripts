"""This script will return a list of security groups with defined fields
and store the information on a csv file - can be use for audit or gathering information"""

import boto3
import csv
import datetime

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. profile1
        2. profile2
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_profile_name == 1:
        local_profile_name = 'localprofile1'
    elif choose_local_profile_name == 2:
        local_profile_name = 'localprofile2'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name


def run():
    
    local_profile_name = profile_account()
    
    #to get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
        
    #Get cloudwatch client conection
    ec2_con_cli = aws_mgmt_con.client(service_name='ec2')
    
    length_security_groups = len(ec2_con_cli.describe_security_groups()["SecurityGroups"])
    print("The total amount of Security groups in the account = ", length_security_groups)
    
    vpc_id = str(input('Enter the VPC ID: '))

    response_sg = ec2_con_cli.describe_security_groups(Filters=[
        {'Name' :'vpc-id', 'Values' :[vpc_id]}
        ])['SecurityGroups']

    #Here we can obtain the total amount of SG on your AWS account considered opened based on response Filters
    length_security_groups_open = len(response_sg)
    print("\nThe total amount of Security groups within the selected VPC = ", length_security_groups_open)
    print('')
    
        #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + str(vpc_id) + '_sg_inventory.csv'
    
    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['Security Group ID', 'Security Group Name', 'VPC'])  

    #This for loop is to list the SG considered opened
    for i in range(length_security_groups_open):
        group_id = response_sg[i]['GroupId']
        group_name = response_sg[i]['GroupName']
        #group_VPC = response_sg[i]['VpcId']
        i+=1
        csv_write_object.writerow([group_id, group_name, vpc_id])
    
    csv_object.close()

if __name__ == '__main__':
    run()