#!/usr/bin/env python

import subprocess
import argparse
import paramiko
import os

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--count', action='store_true', required=False, dest='count')
parser.add_argument('--list', action='store_true', required=False, dest='list')
args = parser.parse_args()

hostname = os.environ['HOSTNAME']
port = 22
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
command = "cat /var/dhcp.leases | awk '{print $4, $3, $2}'"
username = 'username'
password = 'password'
hostname = 'hostname'

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    # client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    client.connect(hostname, port=port, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(command)
    bash_out = stdout.read()

finally:
    client.close()

servers = {
    '_meta': {
        'hostvars': {}
    },
    'idrac': {
        'hosts': []
    },
    'local': {
        'hosts': ['127.0.0.1']
    }
}

# Added some logic to account for newer versions of Ansible formatting newlines differently
if '\\n' in bash_out:
    bash_out_list = bash_out.rstrip().split('\\n')
else:
    bash_out_list = bash_out.rstrip().split('\n')

# bash_out_list = str(bash_out).split('\n')

server_list = []

for line in bash_out_list:
    
    server_list.append(line.replace('\'', '').replace("b", '').rstrip().split(' '))

# exception catch in case there aren't any empty lines
try:
    server_list.remove('')
except ValueError:
    pass

for server in server_list:
    #print server
    if server[0] == '*':
        servers['idrac']['hosts'].append(server[1])
        servers['_meta']['hostvars'][server[0]] = {'mac': server[2]}
    else:
        servers['idrac']['hosts'].append(server[0])
        #servers['_meta']['hostvars'].append(server[0])
        servers['_meta']['hostvars'][server[0]] = {'ansible_host': server[1],'mac': server[2]}

if args.list:
    print(servers)
else:
    print(len(servers['idrac']['hosts']))



