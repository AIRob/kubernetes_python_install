#! /usr/bin/python
# coding: utf-8

import os
import commands

from common import fill_service_configure

class EntryPoint(object):
    default_app_name = "kube-proxy"
    package_path = "/tmp/kubernetes_deploy"
    package_name = "kubernetes/server"
    configure_dir = "/etc/kube-proxy/"
    system_service_dir = "/etc/systemd/system/"
    service_temp_name = "kube-proxy.service.temp"
    service_temp_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, app_name=None, data_dir=None, **kwargs):
        '''
        :param kwargs:
         app_name -- the service name
         data_dir -- the working directory for store data
         user_params -- the parametes user define
        '''

        self.app_name = app_name if app_name else self.default_app_name
        #self.data_dir = data_dir if data_dir else "/var/lib/etcd"
        self.user_params = kwargs

    @property
    def service_file_temp(self):
        return os.path.join(self.service_temp_path, self.service_temp_name)

    @property
    def service_file_target(self):
        return os.path.join(self.system_service_dir, "{}.service".format(self.app_name))

    def prepare(self):
        # Copy binary file
        status, result = commands.getstatusoutput("cp {0}/{1}/bin/kube-proxy /usr/bin".format(self.package_path,
                                                                                     self.package_name))
        if status:
            raise Exception, result

        # Create running directory
        status, result = commands.getstatusoutput("mkdir -p /var/lib/kube-proxy")
        if status:
            raise Exception, result

        self.begin()

    def begin(self):
        # Configure 'etcd.service' file
        fill_service_configure(self.service_file_temp, self.service_file_target, self.user_params)

        # Reload system service files
        status, result = commands.getstatusoutput("systemctl daemon-reload")
        if status:
            raise Exception, result

        # Add service to boot startup
        status, result = commands.getstatusoutput("systemctl enable {0}.service".format(self.app_name))
        if status:
            raise Exception, result

        #Start service
        status, result = commands.getstatusoutput("systemctl start {0}.service".format(self.app_name))
        if status:
            raise Exception, result

        self.finish()

    def finish(self):
        pass

    def invoke(self):
        self.prepare()