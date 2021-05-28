"""This script will return a list of ecs services with defined fields
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
    ecs_con_cli = aws_mgmt_con.client(service_name='ecs')
    response_cluster = ecs_con_cli.list_clusters(maxResults=100)
        
    #Creation of the csv file
    current_date = datetime.datetime.now()
    filename = str(current_date.year) + str(current_date.month) + str(current_date.day) + '_ecs_inventory.csv'

    csv_object = open(filename, 'w', newline='')
    csv_write_object = csv.writer(csv_object)
    csv_write_object.writerow(['Cluster Name','Service Name', 'Service Description'])  

    clusters_arns = response_cluster['clusterArns']
    arn_cut = []
    
    #loop through custers_arn and separate the name from the rest
    for arn in clusters_arns:
        not_usefull, cluster_name = arn.split('cluster/')
        arn_cut.append(cluster_name)
        
    for cluster_name in arn_cut:
        response_services = ecs_con_cli.list_services(cluster=cluster_name,maxResults=100)
        service_arn = response_services['serviceArns']
        
        
        service_full_name = []

        #loop through services arn and separate the cluster/service from the rest
        for service in service_arn:
            not_usefull, name = service.split(':service/', 1)
            service_full_name.append(name)
        
        for i in service_full_name:
            short_name = i.split(sep=None, maxsplit=-1)
                
            #to obtain the tags related to the service
            service_described = ecs_con_cli.describe_services(cluster=cluster_name,services=short_name,include=['TAGS'])
            for each_service_tag in service_described['services']:
                list_of_service_tags = str(each_service_tag.get('tags', 'No TAGS provided!'))
                
            #write the short_name, clustername and listo of service tags
            csv_write_object.writerow([cluster_name, short_name, list_of_service_tags])
            
    csv_object.close()


if __name__ == '__main__':
    run()