from contextlib import contextmanager
import os
from mininet.node import Node


class BGPRouter(Node):
    def __init__(self, *args, **kwargs):
        super(BGPRouter, self).__init__(*args, inNamespace=True, **kwargs)

    @contextmanager
    def routerContext(self):
        working_dir = os.getcwd()
        self.cmd('cd %s' % self.name)
        yield
        self.cmd('cd %s' % working_dir)

    def config(self, **params):
        super(BGPRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')
        self.setHostRoute(params['ip'], "{name}-lo".format(name=self.name))

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(BGPRouter, self).terminate()

    def addHost(self, ip, interface):
        self.setHostRoute(ip, interface)


class FRRRouter(BGPRouter):
    def __init__(self, name, **params):
        if "privateDirs" not in params:
            params["privateDirs"] = [
                "/etc/frr",
                "/var/run/frr",
            ]
        super(FRRRouter, self).__init__(name, **params)

    def config(self, **params):
        super(FRRRouter, self).config(**params)

        with self.routerContext():
            self.cmd('install -m 640 -o frr -g frr frr.conf /etc/frr')
            self.cmd('/usr/lib/frr/zebra -i ./zebra.pid -f /etc/frr/frr.conf --log file:./zebra.log -d')
            self.cmd('/usr/lib/frr/ripd -i ./ripd.pid -f /etc/frr/frr.conf --log file:./ripd.log -d')
            self.cmd('/usr/lib/frr/bgpd -i ./bgpd.pid -f /etc/frr/frr.conf --log file:./bgpd.log -d')

    def terminate(self):
        with self.routerContext():
            self.cmd('kill -9 `cat ./zebra.pid`')
            self.cmd('kill -9 `cat ./ripd.pid`')
            self.cmd('kill -9 `cat ./bgpd.pid`')

        super(FRRRouter, self).terminate()


class BIRDRouter(BGPRouter):
    def __init__(self, name, **params):
        if "privateDirs" not in params:
            params["privateDirs"] = [
                "/etc/bird",
                "/var/run/bird",
            ]
        super(BIRDRouter, self).__init__(name, **params)

    def config(self, **params):
        super(BIRDRouter, self).config(**params)

        self.cmd('install -m 640 -o bird -g bird ../lib/constants.conf /etc/bird')
        self.cmd('install -m 640 -o bird -g bird ../lib/filters.conf /etc/bird')

        with self.routerContext():
            self.cmd('install -m 640 -o bird -g bird bird.conf /etc/bird')
            self.cmd('bird -D bird.log -u bird -g bird')

    def terminate(self):
        with self.routerContext():
            self.cmd('birdc down')

        super(BIRDRouter, self).terminate()
