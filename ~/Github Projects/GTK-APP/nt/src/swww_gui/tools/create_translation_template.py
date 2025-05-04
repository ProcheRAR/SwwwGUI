#!/usr/bin/env python3
"""
Tool to create a translation template for SwwwGUI.

This script creates a JSON template file with all translation keys
that can be used as a starting point for new translations.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the parent directory to the sys.path for importing from the swww_gui package
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.swww_gui.translator import Translator

def main():
    """Run the tool."""
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Create a translation template for SwwwGUI')
    parser.add_argument('-o', '--output', type=str, help='Output file path (default: ~/.config/swww-gui/translations/template.json)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    
    # Set log level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create translator instance
    translator = Translator()
    
    # Create template
    output_path = args.output if args.output else None
    template_path = translator.create_translation_template(output_path)
    
    if template_path:
        print(f"Translation template created at: {template_path}")
        print("To create a new translation:")
        print(f"1. Copy the template: cp {template_path} <language-code>.json")
        print("2. Edit the new file, providing translations for each key")
        print("3. Place the file in ~/.config/swww-gui/translations/")
        print("4. Restart SwwwGUI to see your new language in the settings")
    else:
        print("Failed to create translation template.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 