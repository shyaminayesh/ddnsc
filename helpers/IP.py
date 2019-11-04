#!/usr/bin/env python

import sys, requests

class IP:

    def getPublic(self):

        try:
            response = requests.get("https://ipinfo.io")
            if response.status_code == 200:
                ip = response.json()
                return ip['ip']
        except requests.exceptions.RequestException as e:
            print( e )
            sys,exit(1)