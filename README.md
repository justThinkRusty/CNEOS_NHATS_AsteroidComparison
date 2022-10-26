# CNEOS_NHATS_AsteroidComparison

Author: Charlie Hanner - 2022

 This is a repository for public release of the Python code generated for daily-creation of the comparison chart for human-accessible asteroids in the NHATS database. This project was staretd by Brent Barbee of NASA's Goddard Space Flight Center, and was created in Python by myself. The code is released under the CRAPL license (see LICENSE.md for details). I would like to make sure that the code I wrote is publically available, at least for the moment, for fellow engineers and enthusiasts.

## Requirements

This code was written in Python 3.10.7, and uses the following libraries:
- requests
- matplotlib
- numpy
- datetime
- PIL
- os
- time
- alive_progress (if running the Demo file - the Silent file does not use this library)

import requests  # For API string pull
from matplotlib import pyplot  # Required for plotting
import numpy as np  # is numpy
from datetime import date  # File naming and displayed date of currency
from PIL import Image  # For image manipulation
import os  # For deleting intermittent image files
import time  # For tracking time duration
from alive_progress import alive_bar  # Creating a waitbar for to show progress during long API calls

from PlanetaryData import *  # Pre-defined planetary data import from file
