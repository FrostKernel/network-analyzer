# Welcome to Network Analyzer!
Network Analyzer is a project in development with intent to be a tool for learning the python programming language. Most of it's features are not ready for end-user usage and are subject to change, dubious code quality warning.

## Features
- Checks if the default network gateway is alive, if it is check's internet connection using traceroute. Generates a report in case of internet connection failure of: hop number, hop address and percent of packet loss per hop.
- Logging of generated reports to a gateway-status file with .log extension.

## Requirements:
- Administrator privileges for execution, needed because of the ICMPlib's traceroute function requiring it. Refer to: [Traceroute Documentation](https://github.com/ValentinBELYN/icmplib/blob/main/docs/2-functions.md#traceroute)

## Platform support:
- Tested on Linux and built on it, more specifically NixOS.
- Supposed to work on Mac and Windows, not tested yet though.
