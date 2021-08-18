"""This script will return a list of secrets manager, grab a specific field from those secrets
and change that value for other one

REMEMBER you will need to add a .env file with the required environment variables"""

import boto3
import re
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from botocore.exceptions import ClientError

def account():
    choose_local_source_profile_name = int(input("""Select your local profile name:
        1. Account_1
        2. Account_2
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_source_profile_name == 1:
        local_source_profile_name = 'Account_1'
    elif choose_local_source_profile_name == 2:
        local_source_profile_name = 'Account_2'
    else:
        print('This option is not valid!! we will use default ')
        local_source_profile_name = 'default'
        
    return local_source_profile_name


def environment_on_secret_selection():
    #This function takes environment names: could be dev, qa prod that will preceed the secret name
    environment_variable = int(input("""Select the env that will preceeds the secret name:
        1. Environment_1
        2. Environment_2
        3. Environment_1
        : """))
    if environment_variable == 1:
        environment_variable = 'Environment_1';
    elif environment_variable == 2:
        environment_variable = 'Environment_2';
    elif environment_variable == 3:
        environment_variable = 'Environment_3';
    else:
        print('No valid option selected we will default to Environment_1')
        environment_variable = 'Environment_1';
        
    return environment_variable


def list_src_secrets(secret_con_cli, environment_variable, filter_pattern):
    #this function return a list of all the secrets inside a region and store them as a list
    
    environment = environment_variable
    filter_secrets_expressions = filter_pattern
    
    paginator = secret_con_cli.get_paginator('list_secrets')
    #list_secret_response = secret_con_cli.list_secrets(MaxResults=5)
    
    list_of_secrets = []
    
    print('Returning the list of secrets name that match the filter expression ' + filter_secrets_expressions + '\n')
    
    for secrets in paginator.paginate():
        for secret in secrets['SecretList']:
            secret_name = secret['Name']
            comparisson_result = re.match(filter_secrets_expressions, secret_name)
            if comparisson_result:
                list_of_secrets.append(secret_name)
            else:
                continue
    #print(list_of_secrets, sep = "\n") -- use this for testing 
    return list_of_secrets


def get_src_secret(secret_name, secret_con_cli):
    #this function will return the secret string or content of the secret
    try:
        get_secret_value_response = secret_con_cli.get_secret_value(SecretId=secret_name)
        get_secret_string = get_secret_value_response['SecretString']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
    
    get_secret_dict = json.loads(get_secret_string)
    return get_secret_dict


def modify_rds_secrets(list_secret_name, secret_con_cli):
    #Function for changing keys on RDS READONLY AND RDS READ WRITE
    #This function use an if to match several strings inside the secret name, allowing to change several secrets that use standard body but different names
    for secret_name in list_secret_name:
        if secret_name.find("word1/ro") != -1:
            secret_string = get_src_secret(secret_name, secret_con_cli)
            username = secret_string.get('username', 'None')
            password = secret_string.get('password', 'None')
            new_dns = os.environ.get("NEW_DNS")
            rds_cluster_id = new_dns.split(".")
            dbClusterIdentifier = rds_cluster_id[0]
            secret_string = json.dumps({
                "username": username,
                "password": password,
                "host": new_dns,
                "db_id": dbClusterIdentifier,
                })
            #print(secret_name)
            #print(secret_string)
            change_function(secret_con_cli, secret_name, secret_string)
        if secret_name.find("word1/rw") != -1:
            secret_string = get_src_secret(secret_name, secret_con_cli)
            username = secret_string.get('username', 'None')
            password = secret_string.get('password', 'None')
            new_dns = os.environ.get("NEW_DNS_WR")
            rds_cluster_id = new_dns.split(".")
            dbClusterIdentifier = rds_cluster_id[0]
            secret_string = json.dumps({
                "username": username,
                "password": password,
                "host": new_dns,
                "db_id": dbClusterIdentifier,
                })
            #print(secret_name)
            #print(secret_string)
            change_function(secret_con_cli, secret_name, secret_string)
        else:
            print('Secret name ' + secret_name + ' NOT GOING TO BE MODIFIED') 


def change_function(secret_con_cli, secret_name, secret_string):
    
    try:
        response = secret_con_cli.update_secret(
            SecretId = secret_name,
            SecretString = secret_string
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidParameterException':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'LimitExceededException':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'EncryptionFailure':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'ResourceExistsException':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'MalformedPolicyDocumentException':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("Not Sucess due to:", e)
        elif e.response['Error']['Code'] == 'PreconditionNotMetException':
            print("Not Sucess due to:", e)
        else:
            print('Error not identified')
            raise e
    print('Changing secret content for: ' + response['ARN'])
    #print(response)


def modify_simple_secrets(list_secret_name, secret_con_cli):
    #Function for changing a secret with a connection url with the form https://username:password@dns/enddns
    #connection url = newURL/databaseName
    new_dns_for_simple = os.environ.get("NEW_DNS_FOR_SIMPLE")
    end_url = os.environ.get("END_URL")
    
    for secret_name in list_secret_name:
        secret_string = get_src_secret(secret_name, secret_con_cli)
        simple_connection_uri = secret_string.get('simple_connection_uri', 'None')
        username = secret_string.get('username', 'None')
        password = secret_string.get('password', 'None')
        if simple_connection_uri and username != 'None':
            simple_connection_uri_new = 'https://' + username + ":" + password + '@' + new_dns_for_simple + '/' + end_url
            secret_string = json.dumps({
                "username": username,
                "password": password,
                "simple_connection_uri": simple_connection_uri_new
                })
            change_function(secret_con_cli, secret_name, secret_string)


#RUN MAIN FUNCTION
def run():
    
    profile_name = account()
    src_region = 'region_1'
    environment_variable = environment_on_secret_selection()
    
    aws_mgmt_con = boto3.session.Session(profile_name = profile_name)
    
    #Get secrets manager client conection for src and destination
    secret_con_cli = aws_mgmt_con.client(service_name='secretsmanager',region_name=src_region)
    
    #Obtain a list of all the secrets from the list_src_secrets
    #list_secret_name = list_src_secrets(secret_con_cli)

    choose_action = int(input("""Select the action that you want to execute:
        1. Modify Host for RDS Secrets
        2. Modify host for Simple Secrets
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_action == 1:
        print('Executing the Modify Host for RDS Secret action')
        filter_pattern = environment_variable + '/(rds)/'
        list_secret_name = list_src_secrets(secret_con_cli, environment_variable, filter_pattern)
        print('Modifying the RDS secrets on ' + profile_name + '\n')
        modify_rds_secrets(list_secret_name, secret_con_cli)
        print('\nFinnish execution....')
    
    
    elif choose_action == 2:
        print('Executing the Modify Host for Simple Secret action\n')
        filter_pattern = environment_variable + '/(simple|simple_secret)/'
        list_secret_name = list_src_secrets(secret_con_cli, environment_variable, filter_pattern)
        print('Modifying the mongo secrets on ' + profile_name + '\n')
        modify_simple_secrets(list_secret_name, secret_con_cli)
        print('\nFinnish execution....')
    
    else:
        print('Nothing to do...')


if __name__ == '__main__':
    load_dotenv()
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)
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