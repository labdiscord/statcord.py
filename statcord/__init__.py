__title__ = 'statcord.py'
__author__ = 'Statcord.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, Statcord.com'
__version__ = '1.0.0'

name = "statcord"

from collections import namedtuple
from .client import Client
from .exceptions import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=1, minor=0, micro=0, releaselevel='final', serial=0)
