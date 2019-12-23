#!/usr/bin/env python

import sys, requests, json
from systemd import journal

# HELPERS
from helpers.IP import IP

class CloudFlare:

    # PROPS
    config = None
    record = {
        "id": None
    }
    headers = {
        "Content-type": "application/json",
        "X-Auth-Email": None,
        "X-Auth-Key": None
    }
    ip = {
        "public": None
    }


    # CONSTRUCTOR
    def __init__(self, config):
        self.config = config

        # THINGS TO DO
        self.setPublicIp()
        self.setCloudFlareHeaders()
        self.getRecordIdentifier()



    def setCloudFlareHeaders(self):
        self.headers['X-Auth-Email'] = self.config['CloudFlare'].get('email')
        self.headers['X-Auth-Key'] = self.config['CloudFlare'].get('key')



    def setPublicIp(self):
        self.ip['public'] = IP().getPublic()



    def getRecordIdentifier(self):

        try:

            # REQUEST : GET RECORDS IDENTIFIER ( CloudFlare API )
            res = requests.get("https://api.cloudflare.com/client/v4/zones/" + self.config['CloudFlare'].get('zone') + "/dns_records?name=" + self.config['CloudFlare'].get('host'), headers=self.headers)
            if res.status_code == 200:
                self.record['id'] = res.json()['result'][0]['id']

        except requests.exceptions.RequestException as e:
            print( e )
            sys,exit(1)



    # WORKER
    def worker(self):

        try:

            data = {
                "type": "A",
                "name": self.config['CloudFlare'].get('host'),
                "content": self.ip['public'],
                "ttl": 120,
                "proxied": False
            }

            res = requests.put("https://api.cloudflare.com/client/v4/zones/" + self.config['CloudFlare'].get('zone') + "/dns_records/" + self.record['id'], headers=self.headers, data=json.dumps(data))
            if res.status_code == 200:
                journal.send("[ddnsc]: CloudFlare DDNS update success.")

        except requests.exceptions.RequestException as e:
            print( e )
            sys.exit(1)