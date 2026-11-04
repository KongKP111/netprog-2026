from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
import time

def topology():
    net = Mininet_wifi()
    sta1 = net.addStation('sta1', position='0,50,0')
    sta2 = net.addStation('sta2', position='5,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap', mode='g', channel='1',
                             position='0,50,0', range=30)
    net.configureWifiNodes()
    net.build()
    net.start()

    sta1.cmd('pkill -f echo_server.py')  # clean up any stale server from a previous run
    sta1.cmd('python3 echo_server.py &')
    time.sleep(1)

    info("*** Running benchmark at distance=5\n")
    output = sta2.cmd(f'python3 echo_bench_client.py {sta1.IP()} near')
    print(output)

    sta2.setPosition('28,50,0')
    time.sleep(1)

    info("*** Running benchmark at distance=28\n")
    output = sta2.cmd(f'python3 echo_bench_client.py {sta1.IP()} far')
    print(output)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
