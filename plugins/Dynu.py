#!/usr/bin/env python3
import json
from helpers.rest_provider import RestProvider
from helpers.logger import Logger


class Dynu:

    # PROPS
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "API-Key": None
    }
    records = []


    def __init__(self, zone, config):
        self.zone = zone
        self.config = config
        

        '''
        Configure REST Provider with the headers
        '''
        self.headers['API-Key'] = self.config.get('key')
        self.rest = RestProvider("https://api.dynu.com/v2", auth=None, headers=self.headers)


        '''
        Get list of DNS ids and configure them to make
        updates
        '''
        hosts = self.config['hosts'].split(",")
        for host in hosts:

            '''
            Retrive the record identifiers
            '''
            domains = self.rest.get_json('/dns')
            for domain in domains['domains']:
                if host + '.' + self.config.name == domain['name']:
                    self.records.append({
                        'id': domain['id'],
                        'name': domain['name'],
                        'ipv4Address': None,
                        "ttl": 90,
                        "ipv4": True
                    })




    def worker(self, ip):

        '''
        Make the post request for each record that
        we have in records list
        '''
        for host in self.records:
            host['ipv4Address'] = ip
            Response = self.rest.post('/dns/' + str(host['id']), host)
            if Response == True:
                Logger.info(f"Updating IP address {ip} to Dynu.net record {host['name']}")
            else:
                Logger.Error(f"Failed to update IP address {ip} to Dynu.net record {host['name']}")
