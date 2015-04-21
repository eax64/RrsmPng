#!/usr/bin/env python

import sys
from distutils.core import setup

# if sys.version_info < (3, 0):
#     sys.stdout.write("Sorry, requires Python 3.x.\n")
#     sys.exit(1)

setup(name='rrsmpng',
      version='0.1',
      author="Kevin `eax64` Soules",
      description="Really Really Show My Png. A tool that try to (really) show you a png.",
      license="GPLv2",
      packages=['rrsmpng'],
      scripts=['bin/rrsmpng'],
  )

