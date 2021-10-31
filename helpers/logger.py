# Copyright(c) 2021 by craftyguy "Clayton Craft" <clayton@craftyguy.net>
# Distributed under GPLv3+ (see COPYING) WITHOUT ANY WARRANTY.
import logging
import logging.handlers

try:
    import systemd.journal
    has_systemd = True
except ImportError:
    has_systemd = False


class Logger:
    instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_logger():
        if Logger.instance is None:
            new_instance = logging.getLogger("ddnsc")

            if has_systemd:
                handler = systemd.journal.JournalHandler()
            else:
                # fall back to syslog
                handler = logging.handlers.SysLogHandler(address="/dev/log")

            log_format = logging.Formatter("%(name)s: %(levelname)s "
                                           "%(message)s")
            handler.setFormatter(log_format)
            new_instance.setLevel(logging.INFO)
            new_instance.addHandler(handler)
            Logger.instance = new_instance

        return Logger.instance

    @staticmethod
    def info(msg):
        Logger.get_logger().info(msg)

    @staticmethod
    def error(msg):
        Logger.get_logger().error(msg)

    @staticmethod
    def warning(msg):
        Logger.get_logger().warning(msg)
