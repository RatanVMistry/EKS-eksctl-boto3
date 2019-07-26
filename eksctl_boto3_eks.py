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


def create_cluster():

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


def delete_cluster():
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


def get_nodegroup_info(cluster_name):
    command = "eksctl get nodegroup --cluster {cluster} -o json".format(cluster=cluster_name)
    output = subprocess_cmd(command)
    return json.loads(output)


def print_nodegroupe_info(nodegroup_info):
    for nodegroup in nodegroup_info:
        print("Cluster Name : {Cluster}".format(Cluster=nodegroup['Cluster']))
        print("Stack Name : {StackName}".format(StackName=nodegroup['StackName']))
        print("Nodegroup name : {name}".format(name=nodegroup['Name']))
        print("Maximum size of nodegroup : {max}".format(max=nodegroup['MaxSize']))
        print("Minimum size of nodegroup : {min}".format(min=nodegroup['MinSize']))
        print("Current size of nodegroup : {current}".format(current=nodegroup['DesiredCapacity']))
        print("Instance type for nodegroup instances : {instanceType}".format(instanceType=nodegroup['InstanceType']))
        print("Image Id for instance in nodegroup : {image_id}".format(image_id=nodegroup['ImageID']))


def scale_cluster():
    print_clusters_name(list_clusters_name())
    cluster_name = input ("Enter cluster name which you want to scale up (case sensitive) : ")
    nodegroup_info = get_nodegroup_info(cluster_name)
    current_node = nodegroup_info[0]['DesiredCapacity']
    max_node = nodegroup_info[0]['MaxSize']
    min_node = nodegroup_info[0]['MinSize']
    nodegroup_name = nodegroup_info[0]['Name']

    print(type(max))
    print("Current size of nodegroup = {current}".format(current=current_node))
    print("You can scale nodegroup between {min} and {max}".format(min=min_node, max=max_node))

    node_number = int(input("Enter number to scale :"))
    if node_number <= max_node and node_number >= min_node:
        print("Scale will start")
        command = "eksctl scale nodegroup --cluster {cluster_name} --name {nodegroup_name} --nodes {node_numbers}".format(cluster_name=cluster_name, nodegroup_name=nodegroup_name, node_numbers=node_number)
        output = subprocess_cmd(command)
        print(output)
        print("Scaling done...")

    else:
        print("Enter wrong number. Please enter number in range of {min} - {max} ".format(
            min=nodegroup_info[0]['MinSize'], max=nodegroup_info[0]['MaxSize']))

    #print(nodegroup_info)


#clustersInfo = list_clusters_name()
#print_clusters_name(clustersInfo)

#for cluster in clustersInfo['clusters']:
#    print_cluster_information(cluster)

#create_cluster()
#delete_cluster()


#l = describe_clusters("prod")
#print(l)

#node_groupe = get_nodegroup_info("prod")
#print_nodegroupe_info(node_groupe)
#clusters = list_clusters_name()
#print_clusters_name(clusters)
#delete_cluster()
#create_cluster()
#scale_cluster()
#scale_cluster()
#delete_cluster()