#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = (1, 0, 0)

__version__ = '.'.join(map(str, VERSION))


setup(name='dnsapi',
      version=__version__,
      description='Python DNS API',
      author='Dmitry Roitman',
      author_email='fakeemail@gmail.com',
      install_requires=["nsone",
                        "twisted==16.6.0"],
      scripts=['read_api.py'],
      
     )
