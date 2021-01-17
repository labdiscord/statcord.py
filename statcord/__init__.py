__title__ = 'statcord.py'
__author__ = 'statcord.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, statcord.com'
__version__ = '3.0.6'

name = "statcord"

from collections import namedtuple
from .client import Client
from .exceptions import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=3, minor=0, micro=6, releaselevel='final', serial=0)
