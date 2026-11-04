import json
import time
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

DISTANCES = [5, 10, 15, 20, 25, 30]

def run_iperf3_udp(server_sta, client_sta, server_ip, duration=5, bitrate="10M"):
    server_sta.cmd(f"iperf3 -s -1 -J > /tmp/server_{client_sta.name}.json &")
    time.sleep(1)  # give the server a moment to start listening
    client_sta.cmd(f"iperf3 -c {server_ip} -u -b {bitrate} -t {duration} -J "
                   f"> /tmp/client_{client_sta.name}.json")      # TODO 1
    time.sleep(1)
    with open(f"/tmp/client_{client_sta.name}.json") as f:
        data = json.load(f)
    summary = data["end"]["sum"]                                  # TODO 2
    return {
        "throughput_mbps": summary["bits_per_second"] / 1e6,
        "jitter_ms": summary["jitter_ms"],
        "loss_percent": summary["lost_percent"],
    }

def topology():
    net = Mininet_wifi()
    sta1 = net.addStation('sta1', position='5,50,0')
    sta2 = net.addStation('sta2', position='0,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap', mode='g', channel='1',
                             position='0,50,0', range=30)
    net.configureWifiNodes()

    net.build()
    net.start()

    results = []
    for d in DISTANCES:
        info(f"*** Measuring at distance {d}m\n")
        sta1.setPosition(f"{d},50,0")                             # TODO 3
        time.sleep(1)  # let the wireless link settle after moving
        r = run_iperf3_udp(sta2, sta1, sta2.IP())
        r["distance_m"] = d                                       # TODO 4
        results.append(r)
        print(d, r)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
