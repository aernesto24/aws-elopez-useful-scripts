"""This script will return a list of cloudwatch alarms avoiding the alarms that have a certain word in its name
and store those alarms on a csv file - can be use for audit or gathering information"""

import boto3
import csv
import datetime

def profile_account():
    choose_local_profile_name = int(input("""Select your local profile name:
        1. aws-local-profile-name01
        2. aws-local-profile-name02
        : """))
    
    if choose_local_profile_name == 1:
        local_profile_name = 'aws-local-profile-name01'
    elif choose_local_profile_name == 2:
        local_profile_name = 'aws-local-profile-name01'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name


def run():
    local_profile_name = profile_account()
    
    #to get AWS Management console
    aws_mgmt_con = boto3.session.Session(profile_name = local_profile_name)
    
    #Get cloudwatch client conection
    cw_con_cli = aws_mgmt_con.client(service_name='cloudwatch')

    #paginator to obtain more than 100 results, 100 is the max allowed without this
    paginator = cw_con_cli.get_paginator('describe_alarms')
    page_iterator = paginator.paginate()
    filtered_iterator = page_iterator.search("MetricAlarms")

    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_cw_alarms_inventory.csv'
    
    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['Alarm Name','Alarm ARN', 'Alarm Action', 'Alarm Description'])
    
    #To avoid copying stage alarms
    string_to_avoid = 'stage'
    
    for each_alarm in filtered_iterator:
        if string_to_avoid.lower() in each_alarm['AlarmName'].lower():
            continue
        else:
            alarm_name = each_alarm['AlarmName']
            alarm_arn = each_alarm['AlarmArn']
            alarm_action = str(each_alarm['AlarmActions'])
            alarm_description = each_alarm.get('AlarmDescription', 'No description provided!!!')
            csv_write_object.writerow([alarm_name, alarm_arn, alarm_action, alarm_description])
    
    csv_object.close()

if __name__ == '__main__':
    run()