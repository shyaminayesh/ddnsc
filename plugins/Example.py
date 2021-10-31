#!/usr/bin/env python3
from helpers.logger import Logger


class Example:

    def __init__(self, config):
        Logger.info(config)


    def worker(self, ip):
        """
        :param ip: str IPv4 address to use in the request to update
        """
        Logger.info(f"using IP {ip}")
