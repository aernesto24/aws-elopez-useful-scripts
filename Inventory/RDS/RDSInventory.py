"""This script will return a list of rds cluster with defined fields
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
    rds_con_cli = aws_mgmt_con.client(service_name='rds')
    
    response_rds = rds_con_cli.describe_db_clusters(MaxRecords=100,IncludeShared=True)
    
    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_rds_inventory.csv'

    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['Cluster VPC', 'Cluster Availability Zones','Cluster Name', 'Cluster version', 'Write Endpoint', 'Read endopoint', 'cluster deletion protection', 'DB Instance Name', 'DB Instance Type'])  
    
    for rds_cluster in response_rds['DBClusters']:
        db_cluster_name = rds_cluster['DBClusterIdentifier']
        db_cluster_az = rds_cluster['AvailabilityZones']
        db_cluster_vpc = rds_cluster['DBSubnetGroup']
        db_wr_endpoint = rds_cluster['Endpoint']
        db_ro_endpoint = rds_cluster['ReaderEndpoint']
        db_version = rds_cluster['EngineVersion']
        db_iam_auth = rds_cluster['IAMDatabaseAuthenticationEnabled']
        db_deletion_protection = rds_cluster['DeletionProtection']
        db_cluster_resourceid = rds_cluster['DbClusterResourceId']
        db_cluster_members = rds_cluster['DBClusterMembers']
        
        for db_instance in db_cluster_members:
            #print(db_instance)
            db_instance_name = db_instance['DBInstanceIdentifier']
            response_instance = rds_con_cli.describe_db_instances(DBInstanceIdentifier=db_instance_name)
            #print(response_instance)
            response_instance_class = response_instance['DBInstances']
            instance_class = response_instance_class[0]
            instance_class_type = instance_class['DBInstanceClass']
        
            csv_write_object.writerow([db_cluster_vpc, db_cluster_az, db_cluster_name, db_version, db_wr_endpoint, db_ro_endpoint, db_deletion_protection, db_instance_name, instance_class_type])
    
    csv_object.close()

if __name__ == '__main__':
    run()