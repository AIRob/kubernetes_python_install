#! /usr/bin/python
# coding: utf-8

import importlib

from cmd_line_param import PARSER
from common import get_ip_from_cidr
from conf_parser import USER_PARAMS, CurrentHostParams

SERVICE_PLACEMENT = {
    "master": ["etcd", "kube-apiserver", "kubectl", "kube-controller-manager", "kube-scheduler", "calico", "kubedns", "heapster"],
    "node": ["kubectl", "docker", "kubelet", "kube-proxy"],
    "all": ["etcd", "kube-apiserver", "kubectl", "kube-controller-manager", "kube-scheduler", "calico", "kubedns", "heapster", "docker", "kubelet", "kube-proxy"]
}

def start_deploy(service_name):
    if not USER_PARAMS.get("CONTROLLER_IP", None):
        USER_PARAMS["CONTROLLER_IP"] = CurrentHostParams.get("CURRENT_IPADDR")

    USER_PARAMS["CLUSTER_DNS_IP"] = get_ip_from_cidr(USER_PARAMS["SERVICE_CLUSTER_CIDR"], 2)
    #USER_PARAMS["HEAPSTER_SVC_IP"] = get_ip_from_cidr(USER_PARAMS["SERVICE_CLUSTER_CIDR"], 3)
    USER_PARAMS.update(CurrentHostParams)
    svc_endpoint_entry = "{0}_deploy.entry".format(service_name).replace("-", "_")
    entry = importlib.import_module(svc_endpoint_entry)
    entrypoint = entry.EntryPoint(**USER_PARAMS)
    entrypoint.invoke()

def main_func(cmd_args=None):
    if USER_PARAMS.get("ROLE", None):
        cmd_args.role = USER_PARAMS["ROLE"]
    map(start_deploy, SERVICE_PLACEMENT.get(cmd_args.role, []))

if __name__ == "__main__":
    main_func(cmd_args=PARSER.parse_args())