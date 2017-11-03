#! /usr/bin/python
# coding: utf-8

from argparse import ArgumentParser

PARSER = ArgumentParser(description="Auto deploy in Kubernetes Controller Node")

PARSER.add_argument("-r",
                    "--role",
                    type=str,
                    help="the role is to deploy ControllerNode or MinionNode",
                    choices=["master", "node", "all"],
                    default="master")

PARSER.add_argument("-f",
                    "--file",
                    type=str,
                    help="The absolute path of the configure parameter file",
                    default="/etc/kubernetes/env.cnf")