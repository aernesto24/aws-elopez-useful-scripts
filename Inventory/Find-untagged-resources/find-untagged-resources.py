"""This Script will show you untagged resources"""

import boto3

def region_selection():
    #you can add more regios to this option, remember to add it also on the if statement
    choose_region = int(input("""Select your preferred region:
        1. N. Virginia
        2. N. California
        : """))
    
    if choose_region == 1:
        selected_region = 'us-east-1'
    elif choose_region == 2:
        selected_region = 'us-west-1'
    else:
        print('This option is not valid!! we will use default ')
        selected_region = 'us-east-1'
        
    return selected_region


def profile_account():
    #Rememeber to change this profile name for the ones stored on your computer
    choose_local_profile_name = int(input("""Select your local profile name:
        1. default
        2. profile2
        3. profile3
        : """))
    
    if choose_local_profile_name == 1:
        local_profile_name = 'default'
    elif choose_local_profile_name == 2:
        local_profile_name = 'goku'
    elif choose_local_profile_name == 3:
        local_profile_name = 'itachi'
    else:
        print('This option is not valid!! we will use default ')
        local_profile_name = 'default'
        
    return local_profile_name
    

def print_untagged_ec2_ebs(aws_mgmt_con, region_name):
    ec2_con_re = aws_mgmt_con.resource(service_name='ec2', region_name=region_name)

    #to filter to only untagged ebs
    print('\n****Untagged Volumes****')
    for each_volume in ec2_con_re.volumes.all():
        if not each_volume.tags:
            print(each_volume.id, each_volume.state, each_volume.tags)   


def print_untagged_ec2_instances(aws_mgmt_con, region_name):
    ec2_con_re = aws_mgmt_con.resource(service_name='ec2', region_name=region_name)

    #to filter to only untagged ec2
    print('\n****Untagged Instances****')
    for each_instance in ec2_con_re.instances.all():
        if not each_instance.tags:
            print(each_instance.id, each_instance.instance_type, each_instance.state['Name'], each_instance.tags) 


def print_untagged_sqs_queue(aws_mgmt_con, region_name):
    sqs_con_re = aws_mgmt_con.resource(service_name='sqs', region_name=region_name)
    
    sqs_con_cli = aws_mgmt_con.client(service_name='sqs', region_name=region_name)

    #To put the SQS on a list
    sqs_queues = []

    for each_sqs in sqs_con_re.queues.all():
        print(each_sqs.url.split())
        sqs_queues.append(each_sqs.url)
    
    #print(sqs_queues)  
    
    #To find the tags
    print('\n****Untagged SQS****')
    for each_sqs in sqs_queues:
        response_tags_sqs = sqs_con_cli.list_queue_tags(QueueUrl=each_sqs).get('Tags')
        if response_tags_sqs == None:
            print(each_sqs, response_tags_sqs)      
    

def run():
    local_profile_name = profile_account()
    region_name = region_selection()
    
    aws_mgmt_con = boto3.session.Session(profile_name=local_profile_name)
    
    choose_local_profile_name = int(input("""Select the service you want to know untagged resources:
        1. EBS
        2. EC2
        3. SQS
        : """))
    
    if choose_local_profile_name == 1:
        print_untagged_ec2_ebs(aws_mgmt_con, region_name)
    elif choose_local_profile_name == 2:
        print_untagged_ec2_instances(aws_mgmt_con, region_name)
    elif choose_local_profile_name == 3:
        print_untagged_sqs_queue(aws_mgmt_con, region_name)
    else:
        print('This option is not valid!! we will use default ')


if __name__ == '__main__':
    run()