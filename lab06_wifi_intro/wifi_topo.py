from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

def topology():
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='45,50,0')
    sta2 = net.addStation('sta2', position='55,50,0')
    sta3 = net.addStation('sta3', position='60,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap', mode='g', channel='1', position='50,50,0', range=15)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Starting network\n")
    net.build()
    net.start()

    net.pingAll()
    CLI(net)

    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
