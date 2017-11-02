#! /usr/bin/python
# coding: utf-8

import os
import commands

from common import fill_service_configure

class EntryPoint(object):
    default_app_name = "kubectl"
    package_path = "/tmp/kubectl_deploy"
    package_name = "kubernetes/client"
    configure_dir = ""
    system_service_dir = ""
    service_temp_name = ""
    service_temp_path = ""

    def __init__(self, app_name=None, data_dir=None, **kwargs):
        '''
        :param kwargs:
         app_name -- the service name
         data_dir -- the working directory for store data
         user_params -- the parametes user define
        '''

        self.app_name = app_name if app_name else self.default_app_name
        self.data_dir = data_dir
        self.user_params = kwargs

    @property
    def service_file_temp(self):
        return os.path.join(self.service_temp_path, self.service_temp_name)

    @property
    def service_file_target(self):
        return os.path.join(self.system_service_dir, "{}.service".format(self.app_name))

    def prepare(self):
        # Copy binary file
        status, result = commands.getstatusoutput("cp {0}/{1}/bin/kube* /usr/bin".format(self.package_path,
                                                                                                self.package_name))
        if status:
            raise Exception, result

        # Change attribute about file
        status, result = commands.getstatusoutput("chmod a+x /usr/bin/kube*")
        if status:
            raise Exception, result

        self.begin()

    def begin(self):
        # Configure kubernetes parametes
        status, result = commands.getstatusoutput("kubectl config set-cluster {0}".format(self.user_params.get("CLUSTER_NAME",
                                                                                                               "kubernetes")))
        if status:
            raise Exception, result

        # Configure context
        status, result = commands.getstatusoutput("kubectl config set-context {0} --cluster={1}".format(
            self.user_params.get("CLUSTER_NAME","kubernetes"),
            self.user_params.get("CLUSTER_NAME", "kubernetes")
        ))
        if status:
            raise Exception, result

        # Setup current context
        status, result = commands.getstatusoutput(
            "kubectl config use-context {0}".format(self.user_params.get("CLUSTER_NAME","kubernetes")))
        if status:
            raise Exception, result

        self.finish()

    def finish(self):
        pass

    def invoke(self):
        self.prepare()