#!/usr/bin/env python3

import sys
import os
import gi

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from swww_gui.application import main

if __name__ == "__main__":
    main()
