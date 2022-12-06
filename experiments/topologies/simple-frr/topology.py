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
    AS 4 contains 2 hosts.

    AS 1 provides AS 2.
    AS 2 provides AS 4 and peers with AS 3.
    """

    def build(self):
        # AS 1
        as_one = autonomoussystem.AutonomousSystem(1, 2, router.FRRRouter)
        as_one.construct(self)
        # AS 2
        as_two = autonomoussystem.AutonomousSystem(1, 1, router.FRRRouter)
        as_two.construct(self)
        # AS 3
        as_three = autonomoussystem.AutonomousSystem(1, 3, router.FRRRouter)
        as_three.construct(self)
        # AS 4
        as_four = autonomoussystem.AutonomousSystem(1, 2, router.FRRRouter)
        as_four.construct(self)

        # BGP peering links
        as_one_router_one = as_one.getRouter(1)
        as_two_router_one = as_two.getRouter(1)
        as_three_router_one = as_three.getRouter(1)
        as_four_router_one = as_four.getRouter(1)

        self.addLink(as_one_router_one.name, as_two_router_one.name,
                     intfName1=as_one_router_one.getInterface(), params1={'ip': '1.2.1.1/16'},
                     intfName2=as_two_router_one.getInterface(), params2={'ip': '1.2.1.2/16'})
        self.addLink(as_two_router_one.name, as_three_router_one.name,
                     intfName1=as_two_router_one.getInterface(), params1={'ip': '2.3.1.1/16'},
                     intfName2=as_three_router_one.getInterface(), params2={'ip': '2.3.1.2/16'})
        self.addLink(as_two_router_one.name, as_four_router_one.name,
                     intfName1=as_two_router_one.getInterface(), params1={'ip': '2.4.1.1/16'},
                     intfName2=as_four_router_one.getInterface(), params2={'ip': '2.4.1.2/16'})


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
