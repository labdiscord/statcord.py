__title__ = 'statcord.py-beta'
__author__ = 'statcord.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, statcord.com'
__version__ = '3.0.1'

name = "statcord"

from collections import namedtuple # noqa E402
from .client import Client # noqa E402
from .exceptions import * # noqa E402

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=3, minor=0, micro=1, releaselevel='final', serial=0)
