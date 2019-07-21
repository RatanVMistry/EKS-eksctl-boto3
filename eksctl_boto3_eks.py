import os
import subprocess
import time
import json
import boto3


client = boto3.client('eks')


def subprocess_cmd(command):
    print("cmd to be executed = " + str(command))
    output = subprocess.check_output(command, shell=True)
    #print(output)
    return output


def list_clusters_name():
    #return json.loads(subprocess_cmd("eksctl get cluster -o json"))
    list_clusters = client.list_clusters()
    #print(list_clusters)
    return list_clusters


def print_clusters_name(clusters):
    for i in clusters['clusters']:
        print(i)


def describe_clusters(cluserName):
    return client.describe_cluster(name=cluserName)


def print_cluster_information(clusterName):
    cluster = describe_clusters(clusterName)
    print("Cluster name : {name}".format(name=cluster['cluster']['name']))
    print("Cluster endPoint : {endPoint}".format(endPoint=cluster['cluster']['endpoint']))
    print("VPC ID : {vpc}".format(vpc=cluster['cluster']['resourcesVpcConfig']['vpcId']))
    for subnetId in cluster['cluster']['resourcesVpcConfig']['subnetIds']:
        print("subbet id : {id}".format(id=subnetId))
    for securityGroupId in cluster['cluster']['resourcesVpcConfig']['securityGroupIds']:
        print("Security GroupId = {id}".format(id=securityGroupId))


def is_cluster_available(name, region):
    #clusters = list_clusters_name()
    #current_region is in aws/config

    current_region = client.meta.region_name

    if name in list_clusters_name()['clusters'] and current_region == region:

        return True

    else:

        return False

    #if name in list_clusters_name()['clusters'] and region == region:
     #   return False
    #else:
    #    return True


def createCluster():

    cluster_name = input("Enter cluster name : ")
    cluster_region = input("Enter cluster region : ")

    if is_cluster_available(cluster_name, cluster_region) == True:

        print("Cluster is there change name or region to proceed forward")

    else:
        nodes = input("Enter number of nodes : ")
        min_nodes = input("Enter minimum number of nodes in cluster : ")
        max_nodes = input("Enter maximum number of nodes in cluster : ")
        path = input("enter path for kubeconfig file : ")
        command = "eksctl create cluster --name {clusterName} --version 1.13 --nodegroup-name standard-workers --node-type t3.medium --nodes {nodes} --nodes-min {minNodes} --nodes-max {maxNodes} --node-ami auto --kubeconfig {path}/kubeconfig".format(clusterName=cluster_name, nodes=nodes, minNodes=min_nodes, maxNodes=max_nodes, path=path)
        print(command)
        output = subprocess_cmd(command)
        print_cluster_information(cluster_name)


def deleteCluster():
    f = True
    while f == True:
        clusters = list_clusters_name()

        #for i in clusters:
         #   print("Cluster name == {name} and region == {region}".format(name=i['name'], region=i['region']))
        print_clusters_name(clusters)
        del_cluster = input("Enter name of cluster to delete (case sensitive) : ")

        if del_cluster in list_clusters_name()['clusters']:
            command = "eksctl delete cluster {name}".format(name=del_cluster)
            output = subprocess_cmd(command)
            print(output)
            f = False
        else:
            print("wrong cluster name, please enter correct name ")

#clustersInfo = list_clusters_name()
#print_clusters_name(clustersInfo)

#for cluster in clustersInfo['clusters']:
#    print_cluster_information(cluster)

createCluster()
deleteCluster()
#l = describe_clusters("prod")
#print(l)