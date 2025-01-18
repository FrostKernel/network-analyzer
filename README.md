# Welcome to Network Analyzer!
Network Analyzer is a project in development with intent to be a tool for learning the python programming language. Most of it's features are not ready for end-user usage and are subject to change, dubious code quality warning.

## Features
As of the last commit, the software's only functionality is checking whether the default network gateway the user system has set is alive and if it is, it tests internet connection via traceroute, to check if it is in fact connecting to the internet. However, if the gateway is alive and internet connection fails, a report will be generated containing: Network Hop which failed, it's address and percent of packet loss.

## Requirements:
- Administrator privileges for execution, needed because of the ICMPlib's traceroute function requiring it. Refer to: [Traceroute Documentation](https://github.com/ValentinBELYN/icmplib/blob/main/docs/2-functions.md#traceroute)

## Platform support:
- Tested on Linux and built on it, more specifically NixOS.
- Supposed to work on Mac and Windows, not tested yet though.
