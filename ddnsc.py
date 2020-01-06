#!/usr/bin/env python3
import time, configparser, systemd.daemon, requests

from helpers.IP import IP

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
    systemd.daemon.notify(systemd.daemon.Notification.READY)

    zones = {}
    for zone in config.sections():

        '''
        We have to exclude the global section of the
        configuration file from parsing as a zone
        '''
        if zone == 'global':
            continue

        provider = config[zone].get('provider')


        try:
            module = __import__("plugins." + provider, fromlist=[provider])
        except ImportError:
            print(f"ERROR: Unknown provider in zone '{zone}': {provider}")

        zones[zone] = getattr(module, provider)(zone, config[zone])

    '''
    Get the update interval from the configuration file or
    fallback to default interval 300 seconds
    '''
    update_interval_sec = config['global'].get('interval')
    if not update_interval_sec:
        update_interval_sec = 300
    
    ip = None
    while True:
        new_ip = IP.getPublic()
        if not ip or ip != new_ip:
            ip = new_ip
            print(f"INFO: IP changed, updating zones/hosts with IP: {new_ip}")
            for _, zone_invoke in zones.items():
                zone_invoke.worker(ip)
        time.sleep(int(update_interval_sec))
