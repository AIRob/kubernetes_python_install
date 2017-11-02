#! /usr/bin/python
# coding: utf-8

import os
import commands

from common import fill_service_configure

class EntryPoint(object):
    default_app_name = "heapster"
    package_path = "/tmp/heapster_deploy"
    package_name = ""
    configure_dir = ""
    system_service_dir = ""
    service_temp_name = "heapster.yaml.temp"
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
        self.begin()

    def begin(self):
        # Configure file
        fill_service_configure(self.service_file_temp,
                               "{0}/heapster.yaml".format(self.service_temp_path),
                               self.user_params)

        fill_service_configure("{0}/influxdb.yaml.temp".format(self.service_temp_path),
                               "{0}/influxdb.yaml".format(self.service_temp_path),
                               self.user_params)

        # Kubectl create from yaml file
        status, result = commands.getstatusoutput("kubectl create -f {0}/heapster.yaml".format(self.service_temp_path))
        if status:
            raise Exception, result

        status, result = commands.getstatusoutput("kubectl create -f {0}/influxdb.yaml".format(self.service_temp_path))
        if status:
            raise Exception, result

        self.finish()

    def finish(self):
        pass

    def invoke(self):
        self.prepare()