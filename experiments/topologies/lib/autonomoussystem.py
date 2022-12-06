from dataclasses import dataclass
from typing import List, Tuple
from . import router
from mininet.topo import Topo


@dataclass
class RouterInfo:
    name: str
    ip_prefix: str
    local_switch: str

    def __post_init__(self) -> None:
        self.interface_count = 0

    def getInterface(self) -> str:
        name = f'{self.name}-eth{self.interface_count}'
        self.interface_count += 1
        return name


@dataclass
class HostInfo:
    name: str
    ip: str
    gateway: RouterInfo


class AutonomousSystem:
    as_count = 0

    @staticmethod
    def getASPrefix(asn: int) -> int:
        return asn // 100

    @classmethod
    def getASN(cls) -> int:
        cls.as_count += 1
        return cls.as_count * 100

    def __init__(self, router_count: int, hosts_per_router: int, router_type: type[router.BGPRouter]) -> None:
        assert router_count < 10, 'Unsupported AS size'
        assert hosts_per_router < 10, 'Unsupported AS size'
        self.asn = AutonomousSystem.getASN()
        self.router_type: type[router.BGPRouter] = router_type
        self.routers: List[RouterInfo] = []
        self.switches: List[str] = []
        self.links: List[Tuple[str, str]] = []
        self.hosts: List[HostInfo] = []
        self.switches.append(f's{self.asn}')  # AS core switch
        for idx in range(1, router_count + 1):
            router_name = f'r{self.asn + idx * 10}'
            router_ip_prefix = f'10.{AutonomousSystem.getASPrefix(self.asn)}.{idx}'
            switch_name = f's{self.asn + idx * 10}'
            router_info = RouterInfo(router_name, router_ip_prefix, switch_name)
            self.routers.append(router_info)
            self.switches.append(switch_name)  # Local switch to hosts
            self.links.append([router_name, f'S{self.asn}'])  # Link to core switch
            self.links.append([router_name, switch_name])  # Link to local switch
            for host in range(1, hosts_per_router + 1):
                host_name = f'h{AutonomousSystem.getASPrefix(self.asn)}{idx}{host}'
                host_ip = f'{router_ip_prefix}.{host}'
                self.hosts.append(HostInfo(host_name, host_ip, router_info))
                self.links.append([host_name, switch_name])

    def construct(self, topology: Topo):
        for switch in self.switches:
            topology.addSwitch(switch)
        for router in self.routers:
            topology.addNode(router.name, cls=self.router_type, ip=f'{router.ip_prefix}.254/24')
            topology.addLink(router.name, router.local_switch, intfName1=router.getInterface())
            backbone_ip_component = router.ip_prefix.rsplit('.', 1)
            topology.addLink(router.name, self.switches[0], intfName1=router.getInterface(),
                             params1={'ip': f'{backbone_ip_component[0]}.254.{backbone_ip_component[1]}/24'})
        for host in self.hosts:
            topology.addHost(host.name, ip=f'{host.ip}/24', defaultRoute=f'via {host.gateway.ip_prefix}.254')
            topology.addLink(host.name, host.gateway.local_switch)

    def getRouter(self, router_id: int):
        assert router_id > 0 and router_id <= len(self.routers)
        return self.routers[router_id - 1]
