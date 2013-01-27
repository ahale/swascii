"""
Some pretty bitchin' middleware.

Not to be confused with something that should
be allowed near production servers.
"""

__all__ = ['version_info', 'version']

#: Version information ``(major, minor, revision)``.
version_info = (0, 0, 1)
#: Version string ``'major.minor.revision'``.
version = '.'.join(map(str, version_info))
