"""This script will return a list of s3 buckets with defined fields
and store the information on a csv file - can be use for audit or gathering information"""

import boto3
import csv
import datetime

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. default
        2. goku
        : """))
    
    if choose_local_profile_name == 1:
        local_profile_name = 'default'
    elif choose_local_profile_name == 2:
        local_profile_name = 'goku'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name


def run():
    local_profile_name = profile_account()
    
    #to get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
    
    #Get cloudwatch client conection
    s3_con_cli = aws_mgmt_con.client(service_name='s3')
    
    response_s3 = s3_con_cli.list_buckets(MaxResults=1000)
    
    
    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_s3_inventory.csv'

    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['Bucket Name', 'Bucket Creation Date','Region'])  
    
    for bucket in response_s3['Buckets']:
        bucket_name = bucket["Name"]
        bucket_creation_date = bucket["CreationDate"]
        bucket_location = s3_con_cli.get_bucket_location(Bucket=bucket_name)
        bucket_region = bucket_location.get('LocationConstraint', 'Region not defined under LocationContraint')
        
        if "test" in bucket_name.lower():
            continue
        else:
            csv_write_object.writerow([bucket_name, bucket_creation_date, bucket_region])
    
    csv_object.close()

if __name__ == '__main__':
    run()