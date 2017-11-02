#! /usr/bin/python
# coding: utf-8

import os
import commands
import importlib

from common import fill_service_configure

class EntryPoint(object):
    default_app_name = "docker"
    package_path = "/tmp/docker_deploy"
    package_name = "docker"
    configure_dir = "/etc/docker/"
    system_service_dir = "/etc/systemd/system/"
    service_temp_name = "docker.service.temp"
    service_temp_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, app_name=None, data_dir=None, **kwargs):
        '''
        :param kwargs:
         app_name -- the service name
         data_dir -- the working directory for store data
        '''

        self.app_name = app_name if app_name else self.default_app_name
        #self.data_dir = data_dir if data_dir else "/var/lib/etcd"
        self.user_params = kwargs
        self.load_images = False

    @property
    def service_file_temp(self):
        return os.path.join(self.service_temp_path, self.service_temp_name)

    @property
    def service_file_target(self):
        return os.path.join(self.system_service_dir, "{}.service".format(self.app_name))

    def prepare(self):
        # Copy binary file
        status, result = commands.getstatusoutput("cp {0}/{1}/docker* /usr/bin".format(self.package_path,
                                                                                     self.package_name))
        if status:
            raise Exception, result

        status, result = commands.getstatusoutput("cp {0}/{1}/completion/bash/docker /etc/bash_completion.d/".format(self.package_path,
                                                                                                                     self.package_name))
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
        if self.load_images:
            image_module = importlib.import_module("docker_deploy.images")
            for image in image_module.ImagesInfo:
                self.load_image(image)

    def load_image(self, image_info):
        status, result = commands.getstatusoutput("docker load -i {path}".format(**image_info))
        if status:
            raise Exception, result

        status, result = commands.getstatusoutput("docker tag {id} {name}:{version}".format(**image_info))
        if status:
            raise Exception, result

    def invoke(self):
        self.prepare()