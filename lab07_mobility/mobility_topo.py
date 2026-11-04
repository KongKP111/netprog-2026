import time
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

def sync_links(net):
    # Workaround for this VM: Mininet-WiFi decides the association correctly
    # (wintfs[0].associatedTo) but its own 'iw connect' does not take effect.
    # Make the real link follow Mininet-WiFi's decision.
    for sta in net.stations:
        intf = sta.wintfs[0]
        ap = intf.associatedTo
        link = sta.cmd('iw dev %s link' % intf.name).replace('\r', '')
        if ap is None:
            if 'Connected' in link:
                sta.cmd('iw dev %s disconnect' % intf.name)
        elif ('SSID: %s\n' % ap.ssid) not in link:
            sta.cmd('iw dev %s disconnect' % intf.name)
            sta.cmd('iw dev %s connect %s' % (intf.name, ap.ssid))

def topology():
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='15,50,0')
    sta2 = net.addStation('sta2', position='85,50,0')
    sta3 = net.addStation('sta3', position='10,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap1', mode='g', channel='1',
                             position='20,50,0', range=15, failMode='standalone')
    ap2 = net.addAccessPoint('ap2', ssid='netprog-ap2', mode='g', channel='6',
                             position='80,50,0', range=15, failMode='standalone')

    net.configureWifiNodes()
    net.addLink(ap1, ap2)

    # In this Mininet-WiFi version mobility must be configured before build()
    info("*** Starting mobility\n")
    net.startMobility(time=0)
    net.mobility(sta3, 'start', time=1, position='10,50,0')    # TODO 2
    net.mobility(sta3, 'stop', time=20, position='90,50,0')    # TODO 3
    net.stopMobility(time=21)

    net.build()
    net.start()
    sync_links(net)

    sta3.cmd('ping -i 0.5 10.0.0.1 > /tmp/sta3_ping.log &')    # Part E

    info("*** Monitoring sta3 association during mobility\n")
    for t in range(22):
        sync_links(net)
        intf = sta3.wintfs[0].associatedTo                     # TODO 4
        assoc = intf.node.name if intf else None
        print(f"t={t}s x={sta3.position[0]:.1f} sta3 associated to: {assoc}")
        time.sleep(1)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
