"""This script allows to obtain an inventory of services assigned to each cluster on ECS """

import boto3
from pprint import pprint

client = boto3.client('ecs')
   
response_cluster = client.list_clusters(maxResults=100)
clusters_arns = response_cluster['clusterArns']
arn_cut = []
    #print(clusters_arns)

#loop through custers_arn and separate the name from the rest
for arn in clusters_arns:
    not_usefull, cluster_name = arn.split('cluster/')
    arn_cut.append(cluster_name)

#pprint(arn_cut)

#loop through custers names and provide services arn
for cluster_name in arn_cut:
    response_services = client.list_services(cluster=cluster_name,maxResults=100)
    service_arn = response_services['serviceArns']
    
    service_full_name = []

    #loop through services arn and separate the cluster/service from the rest
    for service in service_arn:
        not_usefull, name = service.split(':service/', 1)
        service_full_name.append(name)
    
    service_short_name = []
    
    for i in service_full_name:
        if '/' in i:
            not_usefull, short_name = i.split('/')
            service_short_name.append(short_name)
        else:
            continue
    
    print('')
    print('These are the services under ', cluster_name)
    pprint(service_short_name)