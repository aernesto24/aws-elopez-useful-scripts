"""This script will return a list of secrets manager, and enable Replication on secrets """

import boto3
import re
from botocore.exceptions import ClientError

def account():
    choose_local_source_profile_name = int(input("""Select your local profile name:
        1. default
        2. prod
        3. sandbox
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_source_profile_name == 1:
        local_source_profile_name = 'default'
    elif choose_local_source_profile_name == 2:
        local_source_profile_name = 'prod'
    elif choose_local_source_profile_name == 3:
        local_source_profile_name = 'sandbox'
    else:
        print('This option is not valid!! we will use default ')
        local_source_profile_name = 'default'
        
    return local_source_profile_name


def environment_on_secret_selection():
    #This function takes environment names: could be dev, qa prod that will preceed the secret name
    environment_variable = int(input("""Select the env that will preceeds the secret name:
        1. dev
        2. Stage
        3. Prod
        : """))
    if environment_variable == 1:
        environment_variable = 'dev';
    elif environment_variable == 2:
        environment_variable = 'stage';
    elif environment_variable == 3:
        environment_variable = 'prod';
    else:
        print('No valid option selected we will default to Environment_1')
        environment_variable = 'dev';
        
    return environment_variable


#Function to list all secret that comply with a filter expression
def list_src_secrets(secret_con_cli, filter_pattern):
    
    filter_secrets_expressions = filter_pattern
    
    paginator = secret_con_cli.get_paginator('list_secrets')
    #list_secret_response = secret_con_cli.list_secrets(MaxResults=5)
    
    print('Returning the list of secrets name that match the filter expression ' + filter_secrets_expressions + '\n')
    
    list_of_secrets = []
    
    print('Returning the list of secrets\n')
    
    for secrets in paginator.paginate():
        for secret in secrets['SecretList']:
            secret_name = secret['Name']
            comparisson_result = re.search(filter_secrets_expressions, secret_name)
            if comparisson_result:
                list_of_secrets.append(secret_name)
            else:
                continue
    #print(list_of_secrets, sep = "\n")
    return list_of_secrets


#Function to retrieve the KMS KeyID for replication
def get_replication_key_parameter_store(aws_mgmt_con, src_region, secret_replication_param):
    
    ssm_con_cli = aws_mgmt_con.client(service_name='ssm',region_name=src_region)
    response_parameter = ssm_con_cli.get_parameter(Name=secret_replication_param)
    
    return response_parameter['Parameter']['Value']



#Function to obtain the status of a secret replication
def get_replication_status(secret_con_cli, secret):
    
    print('Retrieving the replication status for: ' + str(secret))
    
    replication_status = secret_con_cli.describe_secret(SecretId=secret)
    try:
        return replication_status['ReplicationStatus']
    except KeyError:
        return 'Not Replicated'


#Function to enable replication on a secret
def enable_replication(secret_con_cli, secret, dst_region, kms_key):
    
    print("Enabling replication on the following secrets:\n" + str(secret))
    
    response_secret_replication = secret_con_cli.replicate_secret_to_regions(
        SecretId=secret,
        AddReplicaRegions=[
            {
                'Region': dst_region,
                'KmsKeyId': kms_key
            },
        ]
    )
    return response_secret_replication


#RUN MAIN FUNCTION
def run():
    
    profile_name = account()
    src_region = 'us-west-1'
    dst_region = 'us-east-1'
    environment_variable = environment_on_secret_selection()
    secret_replication_param = '/'+environment_variable+'/secretmanager/kms/keyid'
    aws_mgmt_con = boto3.session.Session(profile_name = profile_name)
    
    #Get parameter store for kms key
    kms_key = get_replication_key_parameter_store(aws_mgmt_con, src_region, secret_replication_param )
    
    #Get secrets manager client conection for src and destination
    secret_con_cli = aws_mgmt_con.client(service_name='secretsmanager',region_name=src_region)
    
    #main exeuction step
    filter_pattern = environment_variable
    list_of_secrets = list_src_secrets(secret_con_cli, filter_pattern)

    for secret in list_of_secrets:
        replication_status = get_replication_status(secret_con_cli, secret)
        
        if replication_status == 'Not Replicated':
            print('secret ' + secret + ' is not replicated')
            enable_replication(secret_con_cli,secret , dst_region, kms_key)
            print('Secret ' + secret + " has been successfully replicated")
        else:
            print('secret ' + secret + ' is already replicated')
            continue


if __name__ == '__main__':

    question = True

    while question:
        run()
        
        answer = input(str("\nDo you want to execute other option?? (yes/no) "))
        
        if answer == 'yes' or answer == 'y':
            question = True
        elif answer == 'no' or answer == 'n':
            question = False
        else:
            print("This is not a valid option!!!!")
            question = False