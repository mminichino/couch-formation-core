##
##
import json
import logging
import argparse
import attr
import os
from typing import Union
from couchformation.exception import FatalError
from couchformation.aws.node import AWSDeployment
from couchformation.gcp.node import GCPDeployment
from couchformation.azure.node import AzureDeployment
from couchformation.config import BaseConfig, DeploymentConfig, NodeConfig
from couchformation.exec.process import TFRun
import couchformation.state as STATE
from couchformation.state import BaseConfig
from couchformation.config import get_common_dir, get_resource_dir, NodeGroup, NodeGroupList

logger = logging.getLogger('couchformation.exec.process')
logger.addHandler(logging.NullHandler())


class ProjectError(FatalError):
    pass


class Project(object):

    def __init__(self, args: Union[list, dict]):
        self.args = args
        try:
            STATE.core.project, STATE.core.name, STATE.core.cloud, self.remainder = self.init_from_args(args)
            STATE.paths.common_dir = get_common_dir(STATE.core.project, STATE.core.cloud)
            STATE.paths.resource_dir = get_resource_dir(STATE.core.project, STATE.core.name)
            STATE.paths.cfg_file = os.path.join(STATE.paths.resource_dir, 'deployment.cfg')
            STATE.paths.inf_state_file = os.path.join(STATE.paths.common_dir, 'state.cfg')
            STATE.paths.node_state_file = os.path.join(STATE.paths.resource_dir, 'state.cfg')
            STATE.switch_cloud()
        except Exception as err:
            raise ProjectError(f"{err}")

        if STATE.core.cloud == 'aws':
            self.deployer = AWSDeployment
        elif STATE.core.cloud == 'gcp':
            self.deployer = GCPDeployment
        elif STATE.core.cloud == 'azure':
            self.deployer = AzureDeployment
        else:
            raise ValueError(f"cloud {STATE.core.cloud} is not supported")

    @staticmethod
    def init_from_args(args):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--project', action='store')
        parser.add_argument('--name', action='store')
        parser.add_argument('--cloud', action='store', default="aws")
        parameters, remainder = parser.parse_known_args(args)
        return parameters.project, parameters.name, parameters.cloud, remainder

    @staticmethod
    def cfg_from_args(args, cls):
        parser = argparse.ArgumentParser(add_help=False)
        for attribute in cls.__annotations__:
            parser.add_argument(f"--{attribute}", action='store')
        parameters, remainder = parser.parse_known_args(args)
        arg_data = vars(parameters)
        return arg_data

    @staticmethod
    def node_group(arg_data):
        node_group = NodeGroup()
        for attribute in NodeGroup.__annotations__:
            if arg_data.get(attribute):
                setattr(node_group, attribute, arg_data.get(attribute))
        return node_group

    def create(self):
        node_group: NodeGroup = self.node_group(self.cfg_from_args(self.remainder, NodeGroup))
        group_list = NodeGroupList()
        group_list.groups.append(node_group)
        # noinspection PyTypeChecker
        self.write_file(attr.asdict(group_list), STATE.paths.cfg_file)

    def add(self):
        logger.info(f"Adding node group to {STATE.core.name}")
        cfg_data = self.read_file(STATE.paths.cfg_file)
        group_list = NodeGroupList(**cfg_data)
        node_group: NodeGroup = self.node_group(self.cfg_from_args(self.remainder, NodeGroup))
        group_list.groups.append(node_group)
        # noinspection PyTypeChecker
        self.write_file(attr.asdict(group_list), STATE.paths.cfg_file)

    def deploy(self):
        logger.info(f"Deploying project {STATE.core.project} deployment {STATE.core.name}")
        env = self.deployer()
        env.deploy()

    def destroy(self):
        logger.info(f"Removing project {self._deployment.core.project} deployment {self._deployment.core.name}")
        env = self.deployer()
        env.destroy()

    def list(self):
        env = self.deployer(self.deployment)
        return env.list()

    def provision(self, pre_provision_cmds, provision_cmds, post_provision_cmds):
        env = self.deployer(self.deployment)
        env.provision(pre_provision_cmds, provision_cmds, post_provision_cmds)

    @property
    def deployment(self) -> DeploymentConfig:
        return self._deployment

    @staticmethod
    def read_file(name: str):
        try:
            with open(name, 'r') as cfg_file_h:
                data = json.load(cfg_file_h)
                return data
        except FileNotFoundError:
            return None
        except Exception as err:
            raise ProjectError(f"can not read from config file {name}: {err}")

    @staticmethod
    def write_file(data: dict, name: str):
        try:
            with open(name, 'w') as cfg_file_h:
                json.dump(data, cfg_file_h, indent=2)
                cfg_file_h.write('\n')
        except Exception as err:
            raise ProjectError(f"can not write to config file {name}: {err}")
