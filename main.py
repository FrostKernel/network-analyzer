#!/usr/bin/env python3
import netifaces
import sys
import time
from datetime import datetime
from icmplib import ping, traceroute, resolve


def get_default_gateway() -> str:
    gateways = netifaces.gateways()
    if gateways.get('default'):
        local_gateway = str(gateways['default'][netifaces.AF_INET][0])
        return local_gateway
    else:
        print("Make sure you have set your default gateway.")
        sys.exit(0)


def check_internet_reachability() -> str:
    failed_hops = list()
    ip: str = '1.1.1.1'
    route: list = traceroute(ip)
    for hop in route:
        if hop.is_alive == False:
            failed_hops.append(hop)
    if len(failed_hops) > 0:
        print(f"Internet reachability failure detected. Server used for test: {ip}")
        for hop in failed_hops:
            print(f"Failed path number: {hop.distance}, at address: {hop.address}, percent of lost packets: {hop.packet_loss}")
    else:
        print("Internet reachability test passed. Gateway is online and internet is at reach!")

def check_gateway_status(local_gateway,was_down) -> bool:
    is_alive: bool = ping(local_gateway, count=1, privileged=False).is_alive
    current_time: str = datetime.now().strftime("%I:%M %p")
    if is_alive and was_down:
        was_down = False
        print(f"Gateway came back online at: {current_time}, testing internet reachability.")
        check_internet_reachability()
    elif is_alive and was_down is False:
        print("Default gateway is up.\nProceeding to test internet connectivity")
        check_internet_reachability()
    elif not is_alive and was_down is False:
        was_down = True
        print(f"Default gateway is down. Detected downtime at: {current_time}")
    return was_down


def main() -> None:
    local_gateway: str = get_default_gateway()
    was_down: bool = False
    while True:
        was_down = check_gateway_status(local_gateway,was_down)
        time.sleep(5)


if __name__ == "__main__":
    main()
