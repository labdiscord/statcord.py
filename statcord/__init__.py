__title__ = 'statcord.py-beta'
__author__ = 'statcord.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, statcord.com'
__version__ = '2.1.8'

name = "statcord"

from collections import namedtuple # noqa E402
from .client import Client # noqa E402
from .exceptions import * # noqa E402

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=2, minor=1, micro=7, releaselevel='final', serial=0)
