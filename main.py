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
    ip = '1.1.1.1'
    route = traceroute(ip)
    for hop in route:
        if hop.is_alive == False:
            failed_hops.append(hop)
    if len(failed_hops) > 0:
        print(f"Internet reachability failure detected. Server used for test: {ip}")
        for hop in failed_hops:
            print(f"Failed path number: {hop.distance}, at address: {hop.address}, percent of lost packets: {hop.packet_loss}")
    else:
        print("Internet reachability test passed. Gateway is online and internet is at reach!")

def check_gateway_status(local_gateway,gateway_status) -> str:
    status = ping(local_gateway, count=1, privileged=False)
    current_time = datetime.now().strftime("%I:%M %p")
    if status.is_alive == True:
        if gateway_status is not None:
            print(f"Gateway came back online at: {current_time}, testing internet reachability.")
            gateway_status = None
            check_internet_reachability()
        else:
            print("Default gateway is up.\nProceeding to test internet connectivity")
            check_internet_reachability()
    else:
        if status.is_alive == False and gateway_status is None:
            print(f"Default gateway is down. Detected downtime at: {current_time}")
            gateway_status = current_time
    return gateway_status


def main():
    local_gateway = get_default_gateway()
    gateway_status = None
    while True:
        gateway_status = check_gateway_status(local_gateway,gateway_status)
        time.sleep(5)
main()
