##
##

import os
from typing import Optional, Union, List
from enum import Enum
import attr
import argparse
import couchformation.constants as C


def get_base_dir():
    if 'COUCH_FORMATION_CONFIG_DIR' in os.environ:
        return os.environ['COUCH_FORMATION_CONFIG_DIR']
    else:
        return C.STATE_DIRECTORY


def get_log_dir():
    if 'COUCH_FORMATION_LOG_DIR' in os.environ:
        return os.environ['COUCH_FORMATION_LOG_DIR']
    else:
        return C.LOG_DIRECTORY


def get_project_dir(project: str):
    return os.path.join(get_base_dir(), project)


def get_common_dir(project: str, cloud: str):
    return os.path.join(get_project_dir(project), f"{cloud}_common")


def get_resource_dir(project: str, name: str):
    return os.path.join(get_project_dir(project), name)


def str_to_int(value: Union[str, int]) -> int:
    return int(value)


class AuthMode(Enum):
    default = 0
    sso = 1


class PathMode(Enum):
    resource = 0
    common = 1


class ProvisionMode(Enum):
    public = 0
    private = 1


@attr.s
class BaseConfig:
    project: Optional[str] = attr.ib(default=None)
    cloud: Optional[str] = attr.ib(default="aws")
    name: Optional[str] = attr.ib(default=None)
    region: Optional[str] = attr.ib(default=None)
    ssh_key: Optional[str] = attr.ib(default=None)
    os_id: Optional[str] = attr.ib(default=None)
    os_version: Optional[str] = attr.ib(default=None)
    auth_mode: Optional[str] = attr.ib(default="default")
    profile: Optional[str] = attr.ib(default='default')
    base_dir: Optional[str] = attr.ib(default=get_base_dir())
    private_ip: Optional[bool] = attr.ib(default=False)
    path_mode: Optional[PathMode] = attr.ib(default=PathMode.resource)

    @classmethod
    def create(cls, data: Union[list, dict]):
        if type(data) == list:
            c = cls()
            c.initialize_args(data)
        else:
            c = cls()
            c.initialize_dict(data)
        return c

    def initialize_args(self, args):
        parser = argparse.ArgumentParser(add_help=False)
        for attribute in self.__annotations__:
            parser.add_argument(f"--{attribute}", action='store')
        parameters, remainder = parser.parse_known_args(args)
        self.from_namespace(parameters)

    def initialize_dict(self, options):
        self.from_dict(options)

    @property
    def working_dir(self):
        if self.path_mode == PathMode.resource:
            return get_resource_dir(self.project, self.name)
        else:
            return get_resource_dir(self.project, 'common')

    def common_mode(self):
        self.path_mode = PathMode.common

    def resource_mode(self):
        self.path_mode = PathMode.resource

    def from_namespace(self, namespace: argparse.Namespace):
        args = vars(namespace)
        for attribute in self.__annotations__:
            if args.get(attribute):
                setattr(self, attribute, args.get(attribute))

    def from_dict(self, options: dict):
        for attribute in self.__annotations__:
            if options.get(attribute):
                setattr(self, attribute, options.get(attribute))

    @property
    def auth(self) -> AuthMode:
        return AuthMode[self.auth_mode]

    @property
    def as_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if k != 'base_dir' and k != 'path_mode' and k != 'password'}


@attr.s
class NodeConfig:
    cloud: Optional[str] = attr.ib(default="aws")
    group: Optional[str] = attr.ib(default="1")
    machine_type: Optional[str] = attr.ib(default=None)
    quantity: Optional[int] = attr.ib(default=1, converter=str_to_int)
    services: Optional[str] = attr.ib(default="default")
    volume_iops: Optional[str] = attr.ib(default="3000")
    volume_size: Optional[str] = attr.ib(default="256")
    volume_type: Optional[str] = attr.ib(default=None)
    root_size: Optional[str] = attr.ib(default="256")

    @classmethod
    def create(cls, cloud: str, data: Union[list, dict]):
        if type(data) == list:
            c = cls()
            c.initialize_args(data)
        else:
            c = cls()
            c.initialize_dict(data)
        c.set_cloud(cloud)
        return c

    def initialize_args(self, args):
        parser = argparse.ArgumentParser(add_help=False)
        for attribute in self.__annotations__:
            parser.add_argument(f"--{attribute}", action='store')
        parameters, undefined = parser.parse_known_args(args)
        self.from_namespace(parameters)

    def initialize_dict(self, options):
        self.from_dict(options)

    def set_cloud(self, cloud: str):
        self.cloud = cloud
        if not self.volume_type:
            if self.cloud == "aws":
                self.volume_type = "gp3"
            elif self.cloud == "gcp":
                self.volume_type = "pd-ssd"
            elif self.cloud == "azure":
                self.volume_type = "Premium_LRS"

    def from_namespace(self, namespace: argparse.Namespace):
        args = vars(namespace)
        for attribute in self.__annotations__:
            if args.get(attribute):
                setattr(self, attribute, args.get(attribute))

    def from_dict(self, options: dict):
        for attribute in self.__annotations__:
            if options.get(attribute):
                setattr(self, attribute, options.get(attribute))

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class DeploymentConfig:
    core: Optional[BaseConfig] = attr.ib(default=BaseConfig())
    config: Optional[List[NodeConfig]] = attr.ib(default=[])

    def add_config(self, index: Union[str, int], config: NodeConfig):
        index = int(index)
        config.group = str(index)
        if index > len(self.config) + 1:
            raise ValueError(f"config index {index} out of range")
        elif index == len(self.config) + 1:
            self.config.append(config)
        else:
            self.config[index - 1] = config

    @classmethod
    def new(cls, core: BaseConfig):
        return cls(
            core,
            []
        )

    def reset(self, args):
        self.config.clear()
        self.core = BaseConfig().create(args)

    @property
    def length(self):
        return len(self.config)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class NodeEntry:
    name: Optional[str] = attr.ib(default=None)
    username: Optional[str] = attr.ib(default=None)
    private_ip: Optional[str] = attr.ib(default=None)
    public_ip: Optional[str] = attr.ib(default=None)
    use_private_ip: Optional[bool] = attr.ib(default=False)
    availability_zone: Optional[str] = attr.ib(default=None)
    services: Optional[str] = attr.ib(default=None)

    @classmethod
    def create(cls,
               name: str,
               username: str,
               private_ip: str,
               public_ip: str = None,
               use_private_ip: bool = False,
               zone: str = None,
               services: str = "default"):
        return cls(
            name,
            username,
            private_ip,
            public_ip,
            use_private_ip,
            zone,
            services
        )


@attr.s
class NodeList:
    username: Optional[str] = attr.ib(default=None)
    ssh_key: Optional[str] = attr.ib(default=None)
    nodes: Optional[List[NodeEntry]] = attr.ib(default=[])
    working_dir: Optional[str] = attr.ib(default=None)
    provision_ip: Optional[ProvisionMode] = attr.ib(default=ProvisionMode.public)

    @classmethod
    def create(cls, username: str, ssh_key: str, working_dir: str = None, use_private_ip: bool = False):
        return cls(
            username,
            ssh_key,
            [],
            working_dir,
            ProvisionMode(use_private_ip)
        )

    def add(self, name: str, private_ip: str, public_ip: str = None, zone: str = None, services: str = "default"):
        self.nodes.append(
            NodeEntry.create(
                name,
                self.username,
                private_ip,
                public_ip,
                bool(self.provision_ip.value),
                zone,
                services
            )
        )

    @property
    def node_list(self) -> List[NodeEntry]:
        return self.nodes

    def list_public_ip(self):
        address_list = []
        for entry in self.nodes:
            address_list.append(entry.public_ip)
        return address_list

    def list_private_ip(self):
        address_list = []
        for entry in self.nodes:
            address_list.append(entry.private_ip)
        return address_list

    def provision_list(self):
        if self.provision_ip == ProvisionMode.public:
            return self.list_public_ip()
        else:
            return self.list_private_ip()

    def ip_csv_list(self):
        return ','.join(self.list_private_ip())


@attr.s
class NodeGroup:
    mode: Optional[str] = attr.ib(default="generic")
    region: Optional[str] = attr.ib(default=None)
    quantity: Optional[str] = attr.ib(default="1")
    machine_type: Optional[str] = attr.ib(default=None)
    ssh_key: Optional[str] = attr.ib(default=None)
    os_id: Optional[str] = attr.ib(default=None)
    os_version: Optional[str] = attr.ib(default=None)
    auth_mode: Optional[str] = attr.ib(default="default")
    data_size: Optional[str] = attr.ib(default="256")
    root_size: Optional[str] = attr.ib(default="256")
    services: Optional[str] = attr.ib(default="default")


@attr.s
class NodeGroupList:
    groups: Optional[List[NodeGroup]] = attr.ib(default=[])
