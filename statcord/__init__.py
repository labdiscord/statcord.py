__title__ = 'statcord.py'
__author__ = 'statcord.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022, statcord.com'
__version__ = '3.1.1'

name = "statcord"

from collections import namedtuple
from .client import Client
from .exceptions import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=3, minor=1, micro=0, releaselevel='final', serial=0)
