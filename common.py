#! /usr/bin/python
# coding: utf-8

import os
import socket
from netaddr import IPNetwork

from string import Template

def get_ip_from_cidr(net_cidr, index):
    ip_list = IPNetwork(net_cidr)
    return ip_list[index].format()

def fill_service_configure(service_temp_file, service_target_file, user_params):

    with open(service_temp_file, "r") as temp_f:
        temp_content = temp_f.read()
        temp = Template(temp_content)
        temp_f.close()

    with open(service_target_file, "w+") as target_f:
        target_f.write(temp.substitute(user_params))
        target_f.close()

def get_hostname():
    '''
    :return:
     Princess
    '''
    return socket.gethostname()

def get_host_fdnq():
    '''
    :return:
     Princess.intra.legendsec.com
    '''
    return socket.getfqdn(socket.gethostname())

def get_host_ips():
    '''
    :return:
     ('Princess.intra.legendsec.com', [], ['192.168.47.1', '192.168.57.1', '172.24.46.49'])
    '''
    return socket.gethostbyname(socket.gethostname())