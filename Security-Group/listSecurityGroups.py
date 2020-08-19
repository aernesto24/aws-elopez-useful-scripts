"""This script obtain an inventory of all the security groups considered Open """

import boto3

ec2 = boto3.client('ec2')

#Here we can obtain the total amount of SG on your AWS account
length_security_groups = len(ec2.describe_security_groups()["SecurityGroups"])
print("The total amount of Security groups = ", length_security_groups)

response = ec2.describe_security_groups(
    Filters=[
        {'Name' :'ip-permission.from-port', 'Values' :['1']},
        {'Name' :'ip-permission.protocol', 'Values' :['tcp']},
        {'Name' :'ip-permission.to-port', 'Values' :['65535']},
        {'Name' :'ip-permission.cidr', 'Values' :['0.0.0.0/0']}
        ]
)['SecurityGroups']

#Here we can obtain the total amount of SG on your AWS account considered opened based on response Filters
length_security_groups_open = len(response)
print("\nThe total amount of Security groups with open policy = ", length_security_groups_open)

#This for loop is to list the SG considered opened
for i in range(length_security_groups_open):
    group_id = response[i]['GroupId']
    i+=1
    print(group_id)
