#!/usr/bin/env python3
from requests.auth import HTTPBasicAuth

# HELPERS
from helpers.rest_provider import RestProvider


class LuaDNS:

    # PROPS
    config = None
    headers = {
        "Accept": "application/json"
    }

    # CONSTRUCTOR
    def __init__(self, zone, config):
        self.config = config
        self.zone = zone
        self.rest = RestProvider("https://api.luadns.com/v1",
                                 auth=HTTPBasicAuth(self.config.get('email'),
                                                    self.config.get('key')),
                                 headers=self.headers)
        self._zone_records = {}
        self._zones = {}
        self.zones = self._get_zones()
        self.ttl = self.config.get['ttl']
        if not self.ttl:
            self.ttl = 3600

    def worker(self, ip):
        hosts = self.config['hosts'].split(',')
        host_records = self._get_records(self.zones[self.zone])
        put_url = f"zones/{self.zones[self.zone]}/records"
        for host in hosts:
            if host == '@':
                host = self.zone
            else:
                host += '.' + self.zone
            if not host.endswith('.'):
                host += '.'
            if host not in host_records:
                print(f"WARN: Attempted to update host '{host}' that is not "
                      "found under this account!")
                continue
            data = {
                "type": "A",
                "name": host,
                "content": ip,
                "ttl": self.ttl,
            }
            ret = self.rest.put(f"{put_url}/{host_records[host]}", data)
            if not ret:
                print(f"ERROR: Unable to update host record for '{host}' at "
                      "zone '{self.zone}'")
                continue

    def _get_records(self, zone_id):
        """
        :param zone_id: integer zone ID for luaDNS zone to fetch records from
        :returns: dict where record name is key record id is val.
        """
        if zone_id not in self._zone_records:
            r_list = self.rest.get(f"zones/{zone_id}")
            if r_list:
                self._zone_records = {r['name']: r['id'] for r in r_list['records'] if r['type'].lower() == 'a'}
        return self._zone_records

    def _get_zones(self):
        """
        :returns: dict where zone name is key and zone id is val.
        """
        if not self._zones:
            z_list = self.rest.get("zones")
            if z_list:
                self._zones = {z['name']: z['id'] for z in z_list}
        return self._zones
