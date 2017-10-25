#!/usr/bin/env python
"""
Runner for dev-test loop.
"""
from os.path import abspath, dirname
import sys


here = abspath(dirname(__file__))
sys.path.append(here)


from experiments.current_display import main


if __name__ == '__main__':
    main()
