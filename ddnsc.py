#!/usr/bin/env python3
import time, configparser, systemd.daemon, requests

# PLUGINS
from plugins.CloudFlare import CloudFlare

if __name__ == '__main__':

    '''
    Load main configuration file into the application
    and then need to proceed in the following steps.

        - Implement global configuration
        - Call releval dns updaters

    '''
    config = configparser.ConfigParser()
    config.read('/etc/ddnsc/ddnsc.conf')

    # NOTIFY ( systemd )
    systemd.daemon.notify('READY=1')

    zones = {}
    for zone in config.sections():
        if zone == 'global':
            continue
        provider = config[zone].get('provider')
        try:
            module = __import__("plugins." + provider, fromlist=[provider])
        except ImportError:
            print(f"ERROR: Unknown provider in zone '{zone}': {provider}")
        zones[zone] = getattr(module, provider)(zone, config[zone])
    update_interval_sec = config['global'].get('interval')
    if not update_interval_sec:
        update_interval_sec = 300

    while True:
        for _, zone_invoke in zones.items():
            zone_invoke.worker()

        time.sleep(update_interval_sec)
