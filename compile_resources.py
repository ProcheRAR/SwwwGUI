#!/usr/bin/env python3

import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def compile_resources():
    """Compile GResource files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    resource_xml = os.path.join(data_dir, 'io.github.swwwgui.gresource.xml')
    resource_bin = os.path.join(script_dir, 'src', 'swww_gui', 'resources.gresource')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(resource_bin), exist_ok=True)
    
    # Compile resources
    try:
        subprocess.run(['glib-compile-resources',
                        '--target', resource_bin,
                        '--sourcedir', data_dir,
                        resource_xml],
                       check=True)
        logger.info(f"Resources compiled successfully to {resource_bin}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to compile resources: {e}")
        return False
    except FileNotFoundError:
        logger.error("Error: glib-compile-resources not found. Make sure glib-2.0 development files are installed.")
        return False

if __name__ == "__main__":
    compile_resources()
