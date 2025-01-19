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
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level = logging.INFO,
        filename = f"gateway-status-{current_time}.log",
        filemode = mode,
        format = "%(asctime)s %(levelname)s %(message)s"
    )
    return logger


def get_default_gateway() -> str:
    gateways: dict = netifaces.gateways()
    if gateways.get('default'):
        local_gateway: str = str(gateways['default'][netifaces.AF_INET][0])
        return local_gateway
    else:
        print("Make sure you have set your default gateway.")
        sys.exit(0)


def check_internet_connectivity(logger) -> str:
    failed_hops: list = list()
    ip: str = '1.1.1.1'
    route: list = traceroute(ip)
    for hop in route:
        if not hop.is_alive:
            failed_hops.append(hop)
    if len(failed_hops) > 0:
        logger.info(f"Internet connectivity failure detected. Server used for test: {ip}")
        for hop in failed_hops:
            logger.info(f"Failed path number: {hop.distance}, at address: {hop.address}, percent of lost packets: {hop.packet_loss}%")
        logger.info(f"----")
    else:
        logger.info("Internet connectivity test passed. Gateway is online and internet is at reach!")
        logger.info(f"----")


def check_gateway_status(local_gateway,was_down,logger) -> bool:
    is_alive: bool = ping(local_gateway, count=1, privileged=False).is_alive
    if is_alive and was_down:
        was_down = False
        logger.info(f"Gateway came back online, testing internet connectivity")
        check_internet_connectivity(logger)
    elif is_alive and was_down is False:
        logger.info(f"Default gateway is up. Proceeding to test internet connectivity")
        check_internet_connectivity(logger)
    elif not is_alive and was_down is False:
        was_down = True
        logger.warning(f"Default gateway is down.")
    return was_down


def main() -> None:
    local_gateway: str = get_default_gateway()
    logger: logging.Logger = event_logging()
    interval: int = 10 # Interval in between checks, use seconds.
    was_down: bool = False
    try:
        while True:
            was_down = check_gateway_status(local_gateway,was_down,logger)
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nExiting...")
        logger.info("Script ended by user.")


if __name__ == "__main__":
    main()
