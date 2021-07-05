"""This script will return a list of secrets manager, 
grab the info and migrate it to a different account or different region inside the same account"""

import boto3
from botocore.exceptions import ClientError

def source_account():
    choose_local_source_profile_name = int(input("""Select your local profile name:
        1. profile1
        2. profile2
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_source_profile_name == 1:
        local_source_profile_name = 'localprofile1'
    elif choose_local_source_profile_name == 2:
        local_source_profile_name = 'localprofile2'
    else:
        print('This option is not valid!! we will use default ')
        local_source_profile_name = 'default'
        
    return local_source_profile_name


def destination_account():
    choose_local_destination_profile_name = int(input("""Select your local profile name:
        1. profile1
        2. profile2
        : """))
    
    #use the names of your local profiles  under ~/.aws/credentials
    if choose_local_destination_profile_name == 1:
        local_destination_profile_name = 'localprofile1'
    elif choose_local_destination_profile_name == 2:
        local_destination_profile_name = 'localprofile2'
    else:
        print('This option is not valid!! we will use default ')
        local_destination_profile_name = 'default'
        
    return local_destination_profile_name


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
    
    return get_secret_string


def list_src_secrets_description(secret_con_cli):
    
    #this function return a list of all the secrets description inside a region and store them as a list
    
    paginator = secret_con_cli.get_paginator('list_secrets')
    #list_secret_response = secret_con_cli.list_secrets(MaxResults=5)
    
    list_of_secret_description = []
    
    for secrets in paginator.paginate():
        for secret in secrets['SecretList']:
            secret_description = secret.get('Description', 'No description provided' )
            list_of_secret_description.append(secret_description)
        
    #print(list_of_secrets)
    return list_of_secret_description


def create_dest_secret(src_secret, converted_secret_name, dest_secret_con_cli,secret_description):
    #This function try to create the secret with the converted name on destination
    #if the secret already exist print a message indicating that already in place,
    #otherwise it will create the secret
    try:
        dest_secret_con_cli.create_secret(Name=converted_secret_name,SecretString=src_secret,Description=secret_description)
        print("The requested secret " + converted_secret_name + " was successfully created on destination account")
        print("The secret description is:" + secret_description)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            print("The requested secret " + converted_secret_name + " already exist on destination")


def convert_secret_name(secret_name):
    #this function return replace a word on the secret name
    word_to_change = 'test'
    new_word = 'clone'
    
    if word_to_change in secret_name:
        converted_text = secret_name.replace(word_to_change, new_word)
    else:
        converted_text = secret_name
        
    return converted_text


def list_src_secrets(secret_con_cli):
    #this function return a list of all the secrets inside a region and store them as a list
    
    paginator = secret_con_cli.get_paginator('list_secrets')
    #list_secret_response = secret_con_cli.list_secrets(MaxResults=5)
    
    list_of_secrets = []
    
    for secrets in paginator.paginate():
        for secret in secrets['SecretList']:
            secret_name = secret['Name']
            list_of_secrets.append(secret_name)
        
    #print(list_of_secrets)
    return list_of_secrets


def run():
    
    source_profile_name = source_account()
    destination_profile_name = destination_account()
    src_region = 'us-west-2'
    dest_region = 'us-east-1'
    
    src_aws_mgmt_con = boto3.session.Session(profile_name = source_profile_name)
    dest_aws_mgmt_con = boto3.session.Session(profile_name = destination_profile_name)
    
    #Get secrets manager client conection for src and destination
    secret_con_cli = src_aws_mgmt_con.client(service_name='secretsmanager',region_name=src_region)
    dest_secret_con_cli = dest_aws_mgmt_con.client(service_name='secretsmanager',region_name=dest_region)
    
    #Obtain a list of all the secrets from the list_src_secrets
    list_secret_name = list_src_secrets(secret_con_cli)
    list_secret_description = list_src_secrets_description(secret_con_cli)
    
    #loop through all the secrets inside the list and for each one
    #           * Obtain secret string
    #           * Convert the name of the secret
    #           * create a new secret on dest account using the converted name and the secret string
    for secret_name, secret_description in zip(list_secret_name, list_secret_description):
        src_secret = get_src_secret(secret_name,secret_con_cli)
        converted_secret_name = convert_secret_name(secret_name)
        create_dest_secret(src_secret, converted_secret_name, dest_secret_con_cli, secret_description)
    
    
if __name__ == '__main__':
    run()