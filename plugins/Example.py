#!/usr/bin/env python3
class Example:

    def __init__(self, config):
        print( config )


    def worker(self, ip):
        """
        :param ip: str IPv4 address to use in the request to update
        """
        print(f"Example::worker using IP {ip}")
