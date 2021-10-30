#!/usr/bin/env python3
import hashlib

# HELPERS
from helpers.http_provider import HttpProvider
from helpers.logger import Logger


class FreeDNS:

    def __init__(self, zone, config):
        self.config = config
        self.zone = zone
        self.api = HttpProvider("https://freedns.afraid.org/api/")
        hasher = hashlib.sha1()
        # auth is a sha1 of <username>|<pass>
        # username must be lower case
        auth_str = config['username'].lower() + '|' + config['password']
        hasher.update(auth_str.encode())
        self.auth_sha = hasher.hexdigest()

        self._zones = []
        self.zones, self.update_url = self._get_zones()

    # Note: FreeDNS uses the IP from the update request to configure
    # subdomains/domains
    def worker(self, ip):
        hosts = self.config['hosts'].split(',')
        for host in hosts:
            if host == '@':
                host = self.zone
            else:
                host += '.' + self.zone
            if host not in self._zones:
                Logger.warning(f"Attempted to update host '{host}' "
                               "that is not found under this account!")
                continue
            ret = HttpProvider.get(self.update_url + host)
            if not ret:
                Logger.error("Unable to update host record "
                             f"for '{host}' at zone '{self.zone}'")
                continue

    def _get_zones(self):
        """
        :returns: list of zone names, and str of update url
        """
        if not self._zones:
            z_list = self.api.get_q_string({
                'action': 'getdyndns',
                'v': '2',
                'sha': self.auth_sha
            })
            if not z_list:
                return None
            self._zones = []
            self._update_url = None
            # zone info is in the format:
            #    <subdomain.domain>|<current ip>|<update url>
            # The first <update url> appears to be valid for any
            # subdomain/domain under the account
            for z_line in z_list.split('\n'):
                try:
                    z_data = z_line.split('|')
                    if not self._update_url:
                        self._update_url = z_data[2]
                    self._zones.append(z_data[0])
                except IndexError:
                    # malformed response
                    continue

        return self._zones, self._update_url
