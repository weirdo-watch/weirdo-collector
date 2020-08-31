import logging
import sys


def get_logger(name: str = None, **kwargs):
    _name = name or __name__
    level = logging.DEBUG if kwargs.pop("verbose", None) else None
    level = logging.ERROR if kwargs.get("quiet", None) else level

    log = logging.getLogger(_name)

    if not log.hasHandlers():
        log.setLevel(level=level or logging.INFO)
        format = "%(levelname)s:%(asctime)s:%(name)s: %(message)s"
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter(format))
        log.addHandler(ch)

    return log
