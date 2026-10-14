from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

class CustomTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s2)
        # TODO 7: constrained WAN backbone
        self.addLink(s1, s2, bw=5, delay='50ms', loss=10)

def main():
    setLogLevel('info')
    # TODO 8: link=TCLink so bw/delay/loss take effect
    net = Mininet(topo=CustomTopo(), link=TCLink)
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    main()
