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

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from translator import Translator

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
    
    # Default output path in user's config directory
    if not args.output:
        config_dir = Path.home() / '.config' / 'swww-gui' / 'translations'
        os.makedirs(config_dir, exist_ok=True)
        output_path = config_dir / 'template.json'
    else:
        output_path = args.output
    
    # Create template
    template_path = translator.create_translation_template(output_path)
    
    if template_path:
        print(f"Translation template created at: {template_path}")
        print("To create a new translation:")
        print(f"1. Copy the template: cp {template_path} ~/.config/swww-gui/translations/<language-code>.json")
        print("2. Edit the new file, providing translations for each key")
        print("3. Restart SwwwGUI to see your new language in the settings")
    else:
        print("Failed to create translation template.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 