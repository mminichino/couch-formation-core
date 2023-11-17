#!/usr/bin/env python3

import os
import sys
import logging
import warnings
import unittest

warnings.filterwarnings("ignore")
logger = logging.getLogger()
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
sys.path.append(current)

from couchformation.network import NetworkDriver
from couchformation.docker.driver.base import CloudBase
from couchformation.docker.driver.network import Network
from couchformation.docker.driver.container import Container


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"
    format_level = "%(levelname)s"
    format_name = "%(name)s"
    format_message = "%(message)s"
    format_line = "(%(filename)s:%(lineno)d)"
    format_extra = " [%(name)s](%(filename)s:%(lineno)d)"
    FORMATS = {
        logging.DEBUG: f"{grey}{format_level}{reset} - {format_message}",
        logging.INFO: f"{green}{format_level}{reset} - {format_message}",
        logging.WARNING: f"{yellow}{format_level}{reset} - {format_message}",
        logging.ERROR: f"{red}{format_level}{reset} - {format_message}",
        logging.CRITICAL: f"{red}{format_level}{reset} - {format_message}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if logging.DEBUG >= logging.root.level:
            log_fmt += self.format_extra
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class TestMainAWS(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore")
        self.parameters = {
              "debug": 0,
              "verbose": 0,
              "command": "create",
              "build": "cbs",
              "cloud": "docker",
              "project": "pytest-docker",
              "name": "test-cluster",
              "connect": None,
              "group": 1,
              "provisioner": "remote",
              "region": "us-east-2",
              "auth_mode": "sso",
              "profile": None,
              "ssh_key": "/Users/michael/.ssh/mminichino-default-key-pair.pem",
              "cidr": None,
              "image": "couchbase/server",
              "quantity": "3",
              "services": None,
              "volume_iops": None,
              "volume_size": None
            }
        self.project = self.parameters.get('project')
        self.image = self.parameters.get('image')

    def tearDown(self):
        pass

    def test_1(self):
        cidr_util = NetworkDriver()
        base = CloudBase(self.parameters)

        Network(self.parameters).list()

        for net in Network(self.parameters).cidr_list:
            cidr_util.add_network(net)

        net_name = f"{self.project}-net"
        node_name = f"{self.project}-node-01"

        cidr_util.get_next_network()
        subnet_list = list(cidr_util.get_next_subnet())

        print(f"Network: {subnet_list[1]}")

        net_id = Network(self.parameters).create(net_name, subnet_list[1])

        container_id = Container(self.parameters).run(self.image, node_name, network=net_id.name)
