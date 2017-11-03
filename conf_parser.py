#! /usr/bin/python
# coding: utf-8

import yaml

USER_PARAMS_PATH = "env.conf"
USER_PARAMS = yaml.load(open(USER_PARAMS_PATH, "r"))

from common import get_hostname, get_host_fdnq, get_host_ips

CurrentHostParams = {
    "CURRENT_HOSTNAME": get_hostname(),
    "CURRENT_FDNQ": get_host_fdnq(),
    "CURRENT_IPADDR": get_host_ips(),
    "CLUSTER_DOMAIN_NAME": "cluster.local",
    "MAINPID": "MAINPID"
}