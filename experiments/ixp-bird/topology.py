import atexit
import os
import sys

from mininet.cli import CLI
from mininet.link import Link
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo

CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CWD, '../'))

from lib import autonomoussystem, router  # NOQA

net = None


class BasicTopo(Topo):
    """
    AS 1 contains 2 hosts.
    AS 2 contains 1 host.
    AS 3 contains 3 hosts.
    """

    def build(self):
        switch = self.addSwitch("s0")
        rs = router.BIRDRouter('rs')
        self.addNode(rs.name, cls=router.BIRDRouter, ip=f'50.0.0.254/24')
        self.addLink("rs", switch)
        # AS 1
        as_one = autonomoussystem.AutonomousSystem(1, 2, router.BIRDRouter)
        as_one.construct(self)
        # AS 2
        as_two = autonomoussystem.AutonomousSystem(1, 1, router.BIRDRouter)
        as_two.construct(self)
        # AS 3
        as_three = autonomoussystem.AutonomousSystem(1, 3, router.BIRDRouter)
        as_three.construct(self)

        # BGP peering links
        as_one_router_one = as_one.getRouter(1)
        as_two_router_one = as_two.getRouter(1)
        as_three_router_one = as_three.getRouter(1)

        self.addLink(as_one_router_one.name, switch, intfName1=as_one_router_one.getInterface(), params1={'ip': '50.0.0.1/24'})
        self.addLink(as_two_router_one.name, switch, intfName1=as_two_router_one.getInterface(), params1={'ip': '50.0.0.2/24'})
        self.addLink(as_three_router_one.name, switch, intfName1=as_three_router_one.getInterface(), params1={'ip': '50.0.0.3/24'})


def startNetwork():
    info('*** Creating the network\n')
    topology = BasicTopo()

    global net
    net = Mininet(topo=topology, link=Link, autoSetMacs=True)

    info('*** Starting the network\n')
    net.start()
    info('*** Running CLI\n')
    CLI(net)


def stopNetwork():
    if net is not None:
        net.stop()


if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
