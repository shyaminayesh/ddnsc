#!/usr/bin/env python3

import sys, requests
from helpers.logger import Logger

class IP:

    @staticmethod
    def getPublic():

        try:
            response = requests.get("https://ipinfo.io")
            if response.status_code == 200:
                ip = response.json()
                return ip['ip']
        except requests.exceptions.RequestException as e:
            Logger.error("Unable to get public IP address!")
            Logger.error( e )
            sys,exit(1)
