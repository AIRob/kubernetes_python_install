#! /usr/bin/python
# coding: utf-8

import importlib

from cmd_line_param import PARSER
from conf_parser import USER_PARAMS, CurrentHostParams

SERVICE_PLACEMENT = {
    "master": ["etcd", "kube-apiserver", "kubectl", "kube-controller-manager", "kube-scheduler", "calico", "kubedns"],
    "node": ["kubectl", "docker", "kubelet", "kube-proxy"]
}

def start_deploy(service_name):
    USER_PARAMS.update(CurrentHostParams)
    svc_endpoint_entry = "{0}_deploy.entry".format(service_name).replace("-", "_")
    entry = importlib.import_module(svc_endpoint_entry)
    entrypoint = entry.EntryPoint(**USER_PARAMS)
    entrypoint.invoke()

def main_func(cmd_args=None):
    map(start_deploy, SERVICE_PLACEMENT.get(cmd_args.role, []))

if __name__ == "__main__":
    main_func(cmd_args=PARSER.parse_args())
