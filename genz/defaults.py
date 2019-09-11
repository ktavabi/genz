#!/usr/bin/env python

"""Global study parameters."""

__author__ = 'Kambiz Tavabi'
__copyright__ = 'Copyright 2018, Seattle, Washington'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Kambiz Tavabi'
__email__ = 'ktavabi@uw.edu'

from os import path as op
from pathlib import Path
import numpy as np

static = op.join(Path(__file__).parents[0], 'static')
datadir = op.join(Path(__file__).parents[0], 'data')
figs_dir = op.join(Path(__file__).parents[0], 'figures')
megdata = '/mnt/jaba/meg/genz_resting'
subjects_dir = '/mnt/jaba/meg/genz/anatomy'
exclude = ['104_9a',  # Too few EOG events
           '108_9a',  # Fix
           '113_9a',  # Too few ECG events
           '115_9a',  # no cHPI
           '121_9a',  # Source space missing points
           '209_11a',  # Too few EOG events
           '231_11a',  # twa_hp calc fail with assertion error
           '432_15a',  # Too few ECG events
           '510_17a',  # Too few ECG events
           '527_17a']  # Too few EOG events

# frequencies of interest
bands = {
    'DC': (0.01, 2), 'delta': (2, 4), 'theta': (5, 7),
    'alpha': (8, 12), 'beta': (13, 29), 'gamma': (30, 50)
    }

# ages
ages = np.arange(9, 19, 2)
