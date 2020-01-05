#!/usr/bin/env python3
import sys, requests, json
from systemd import journal

# HELPERS
from helpers.IP import IP
from helpers.rest_provider import RestProvider

class CloudFlare:

    # PROPS
    config = None
    records = []
    headers = {
        "Content-type": "application/json",
        "X-Auth-Email": None,
        "X-Auth-Key": None
    }
    ip = {
        "public": None
    }


    # CONSTRUCTOR
    def __init__(self, zone, config):
        self.zone = zone
        self.config = config


        '''
        Need to configure the current public IP
        before the update process begin.
        '''
        self.ip['public'] = IP().getPublic()


        '''
        Need to configure CloudFlare request headers
        prior to make any API request.
        '''
        self.headers['X-Auth-Email'] = self.config.get('email')
        self.headers['X-Auth-Key'] = self.config.get('key')


        '''
        Configure REST Provider with the headers
        '''
        self.rest = RestProvider("https://api.cloudflare.com/client/v4", auth=None, headers=self.headers)


        '''
        Configure CloudFlare host record identifiers for each
        record in the configuration file
        '''
        hosts = self.config['hosts'].split(",")
        for host in hosts:

            '''
            Retrive the record identifiers
            '''
            id_list = self.rest.get('/zones/' + self.config.get('zone') + '/dns_records?name=' + host + '.' + self.config.name)
            if id_list:
                self.records.append({
                    "type": "A",
                    "id": id_list['result'][0]['id'],
                    "name": host + '.' + self.config.name,
                    "content": self.ip['public'],
                    "ttl": 120,
                    "proxied": False
                })




    # WORKER
    def worker(self):
        for host in self.records:
            self.rest.put('/zones/' + self.config.get('zone') + '/dns_records/' + host['id'], host)