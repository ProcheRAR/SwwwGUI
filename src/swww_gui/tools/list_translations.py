#!/usr/bin/env python3
"""
Tool to list all available translations for SwwwGUI.

This script lists all loaded translation files and their metadata.
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
    parser = argparse.ArgumentParser(description='List available translations for SwwwGUI')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    
    # Set log level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create translator instance
    translator = Translator()
    
    # Get translations directory
    translations_dir = translator._get_translations_dir()
    print(f"Translations directory: {translations_dir}")
    print()
    
    # List available languages
    languages = translator.get_supported_languages()
    print(f"Found {len(languages)} translations:")
    
    for lang in languages:
        print(f"- {lang['name']} ({lang['code']})")
    
    # Check number of keys in each translation
    print("\nTranslation keys:")
    for code in translator.translations:
        keys_count = len(translator.translations[code])
        print(f"- {code}: {keys_count} keys")
    
    # List translation keys from English that are missing in other languages
    print("\nMissing translation keys:")
    for code in translator.translations:
        if code == 'en':
            continue
            
        en_keys = set(translator.translations['en'].keys())
        lang_keys = set(translator.translations[code].keys())
        missing_keys = en_keys - lang_keys
        
        if missing_keys:
            print(f"- {code}: {len(missing_keys)} missing keys")
            if args.verbose:
                for key in sorted(missing_keys):
                    print(f"  - {key}")
        else:
            print(f"- {code}: Complete translation")
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 