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

    while True:   

        for section in config.sections():
            if section == 'global': continue

            # DUNAMIC PLUGIN
            module = __import__("plugins." + section, fromlist=[section])
            instance = getattr(module, section)(config)
            instance.worker()
    update_interval_sec = config['global'].get('interval')
    if not update_interval_sec:
        update_interval_sec = 300


        time.sleep(update_interval_sec)
