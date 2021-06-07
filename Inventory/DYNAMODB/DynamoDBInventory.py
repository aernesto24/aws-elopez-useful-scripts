"""This script will return a list of dynamoDB tables with defined fields
and store the information on a csv file - can be use for audit or gathering information"""

import boto3
import csv
import datetime

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. profile_1
        2. profile_"
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_profile_name == 1:
        local_profile_name = 'profile_1'
    elif choose_local_profile_name == 2:
        local_profile_name = 'profile_2'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'profile_1'
        
    return local_profile_name


def run():
    local_profile_name = profile_account()
    
    #to get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
    
    #Get cloudwatch client conection
    ddb_con_cli = aws_mgmt_con.client(service_name='dynamodb')
    
    #paginator to obtain more than 100 results, 100 is the max allowed without this
    paginator = ddb_con_cli.get_paginator('list_tables')
    page_iterator = paginator.paginate()
    filtered_iterator = page_iterator.search("TableNames")
    
    #response_ddb = ddb_con_cli.list_tables(Limit=1000)
    #print(response_ddb)
    
    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_ddb_inventory.csv'

    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['Table Name', 'Table Attributes'])  
    
    for each_ddb_table in filtered_iterator:
        #print(each_ddb_table)
        response_ddb_table = ddb_con_cli.describe_table(TableName=each_ddb_table)
        
        csv_write_object.writerow([each_ddb_table, response_ddb_table])
    
    csv_object.close()

if __name__ == '__main__':
    run()