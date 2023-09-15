##
##

from __future__ import annotations
import attr
from typing import Optional, List


@attr.s
class AWSInstance:
    instance_id: Optional[str] = attr.ib(default=None)
    machine_type: Optional[str] = attr.ib(default=None)
    volume_iops: Optional[str] = attr.ib(default="3000")
    volume_size: Optional[str] = attr.ib(default="256")
    volume_type: Optional[str] = attr.ib(default="gp3")
    root_iops: Optional[str] = attr.ib(default="3000")
    root_size: Optional[str] = attr.ib(default="256")
    root_type: Optional[str] = attr.ib(default="gp3")
    username: Optional[str] = attr.ib(default=None)
    public_ip: Optional[str] = attr.ib(default=None)
    private_ip: Optional[str] = attr.ib(default=None)
    services: Optional[str] = attr.ib(default=None)
    zone: Optional[str] = attr.ib(default=None)
    subnet_id: Optional[str] = attr.ib(default=None)


@attr.s
class AWSInstanceSet:
    name: Optional[str] = attr.ib(default=None)
    instance_list: Optional[List[AWSInstance]] = attr.ib(default=[])


@attr.s
class AWSZone:
    zone: Optional[str] = attr.ib(default=None)
    subnet_id: Optional[str] = attr.ib(default=None)


@attr.s
class AWSState:
    region: Optional[str] = attr.ib(default=None)
    vpc_id: Optional[str] = attr.ib(default=None)
    security_group_id: Optional[str] = attr.ib(default=None)
    ssh_key: Optional[str] = attr.ib(default=None)
    internet_gateway_id: Optional[str] = attr.ib(default=None)
    route_table_id: Optional[str] = attr.ib(default=None)
    zone_list: Optional[List[AWSZone]] = attr.ib(default=[])


@attr.s
class GCPDisk:
    name: Optional[str] = attr.ib(default=None)
    zone: Optional[str] = attr.ib(default=None)


@attr.s
class GCPInstance:
    name: Optional[str] = attr.ib(default=None)
    machine_type: Optional[str] = attr.ib(default=None)
    volume_size: Optional[str] = attr.ib(default="256")
    volume_type: Optional[str] = attr.ib(default="pd-ssd")
    root_size: Optional[str] = attr.ib(default="256")
    root_type: Optional[str] = attr.ib(default="pd-ssd")
    username: Optional[str] = attr.ib(default=None)
    public_ip: Optional[str] = attr.ib(default=None)
    private_ip: Optional[str] = attr.ib(default=None)
    services: Optional[str] = attr.ib(default=None)
    zone: Optional[str] = attr.ib(default=None)
    disk_list: Optional[List[GCPDisk]] = attr.ib(default=[])


@attr.s
class GCPInstanceSet:
    name: Optional[str] = attr.ib(default=None)
    instance_list: Optional[List[AWSInstance]] = attr.ib(default=[])


@attr.s
class GCPZone:
    zone: Optional[str] = attr.ib(default=None)


@attr.s
class GCPState:
    region: Optional[str] = attr.ib(default=None)
    network: Optional[str] = attr.ib(default=None)
    subnet: Optional[str] = attr.ib(default=None)
    ssh_key: Optional[str] = attr.ib(default=None)
    firewall: Optional[str] = attr.ib(default=None)
    gcp_project: Optional[str] = attr.ib(default=None)
    credentials: Optional[str] = attr.ib(default=None)
    zone_list: Optional[List[AWSZone]] = attr.ib(default=[])


@attr.s
class AzureDisk:
    name: Optional[str] = attr.ib(default=None)
    zone: Optional[str] = attr.ib(default=None)
    disk_attachment:  Optional[str] = attr.ib(default=None)


@attr.s
class AzureInstance:
    name: Optional[str] = attr.ib(default=None)
    machine_type: Optional[str] = attr.ib(default=None)
    volume_tier: Optional[str] = attr.ib(default="P20")
    volume_size: Optional[str] = attr.ib(default="256")
    volume_type: Optional[str] = attr.ib(default="Premium_LRS")
    root_tier: Optional[str] = attr.ib(default="P20")
    root_size: Optional[str] = attr.ib(default="256")
    root_type: Optional[str] = attr.ib(default="Premium_LRS")
    username: Optional[str] = attr.ib(default=None)
    public_ip: Optional[str] = attr.ib(default=None)
    private_ip: Optional[str] = attr.ib(default=None)
    services: Optional[str] = attr.ib(default=None)
    zone: Optional[str] = attr.ib(default=None)
    vm_public_ip: Optional[str] = attr.ib(default=None)
    vm_nic: Optional[str] = attr.ib(default=None)
    vm_nsg_association: Optional[str] = attr.ib(default=None)
    disk_list: Optional[List[AzureDisk]] = attr.ib(default=[])


@attr.s
class AzureInstanceSet:
    name: Optional[str] = attr.ib(default=None)
    instance_list: Optional[List[AWSInstance]] = attr.ib(default=[])


@attr.s
class AzureZone:
    zone: Optional[str] = attr.ib(default=None)


@attr.s
class AzureState:
    location: Optional[str] = attr.ib(default=None)
    network: Optional[str] = attr.ib(default=None)
    subnet: Optional[str] = attr.ib(default=None)
    ssh_key: Optional[str] = attr.ib(default=None)
    network_security_group: Optional[str] = attr.ib(default=None)
    zone_list: Optional[List[AWSZone]] = attr.ib(default=[])


@attr.s
class BaseConfig:
    project: Optional[str] = attr.ib(default="couchformation")
    cloud: Optional[str] = attr.ib(default="aws")
    name: Optional[str] = attr.ib(default="resources")


@attr.s
class PathConfig:
    common_dir: Optional[str] = attr.ib(default=None)
    resource_dir: Optional[str] = attr.ib(default=None)
    cfg_file: Optional[str] = attr.ib(default=None)
    inf_state_file: Optional[str] = attr.ib(default=None)
    node_state_file: Optional[str] = attr.ib(default=None)


core = BaseConfig()
paths = PathConfig()

infrastructure = None
instance_set = None


def switch_cloud() -> None:
    global infrastructure, \
        instance_set

    if core.cloud == 'aws':
        infrastructure = AWSState
        instance_set = AWSInstanceSet
    elif core.cloud == 'gcp':
        infrastructure = GCPState
        instance_set = GCPInstanceSet
    elif core.cloud == 'azure':
        infrastructure = AzureState
        instance_set = AzureInstanceSet
