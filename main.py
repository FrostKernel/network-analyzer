#!/usr/bin/env python3
import netifaces
import sys
import time
import logging
import os
from datetime import datetime
from icmplib import ping, traceroute, resolve


def event_logging() -> str:
    current_time: str = datetime.now().strftime('%d-%m-%y')
    log_file: str = f"gateway-status-{current_time}.log"
    if os.path.exists(log_file):
        mode: str = "a"
    else:
        mode: str = "w"
    logging.basicConfig(
        level = logging.INFO,
        filename = f"gateway-status-{current_time}.log",
        filemode = mode,
        format = "%(asctime)s %(levelname)s %(message)s"
    )
    return logging


def get_default_gateway() -> str:
    gateways: dict = netifaces.gateways()
    if gateways.get('default'):
        local_gateway: str = str(gateways['default'][netifaces.AF_INET][0])
        return local_gateway
    else:
        print("Make sure you have set your default gateway.")
        sys.exit(0)


def check_internet_connectivity(logging) -> str:
    failed_hops: list = list()
    ip: str = '1.1.1.1'
    route: list = traceroute(ip)
    for hop in route:
        if not hop.is_alive:
            failed_hops.append(hop)
    if len(failed_hops) > 0:
        logging.info(f"Internet connectivity failure detected. Server used for test: {ip}")
        for hop in failed_hops:
            logging.info(f"Failed path number: {hop.distance}, at address: {hop.address}, percent of lost packets: {hop.packet_loss}%")
        logging.info(f"----")
    else:
        logging.info("Internet connectivity test passed. Gateway is online and internet is at reach!")
        logging.info(f"----")


def check_gateway_status(local_gateway,was_down,logging) -> bool:
    is_alive: bool = ping(local_gateway, count=1, privileged=False).is_alive
    if is_alive and was_down:
        was_down = False
        logging.info(f"Gateway came back online, testing internet connectivity")
        check_internet_connectivity(logging)
    elif is_alive and was_down is False:
        logging.info(f"Default gateway is up. Proceeding to test internet connectivity")
        check_internet_connectivity(logging)
    elif not is_alive and was_down is False:
        was_down = True
        logging.warning(f"Default gateway is down.")
    return was_down


def main() -> None:
    local_gateway: str = get_default_gateway()
    logging: str = event_logging()
    interval: int = 10 # Interval in between checks, use seconds.
    was_down: bool = False
    while True:
        was_down = check_gateway_status(local_gateway,was_down,logging)
        time.sleep(interval)


if __name__ == "__main__":
    main()
