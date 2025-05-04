#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages
import os
import subprocess

# Compile resource file if possible
try:
    from compile_resources import compile_resources
    compile_resources()
except Exception as e:
    print(f"Warning: Could not compile resources: {e}")
    print("You may need to run 'python compile_resources.py' manually")

setup(
    name="swwwgui",
    version="1.0.0",
    description="A modern GTK4 GUI for swww wallpaper daemon with matugen integration",
    author="ProcheRAR",
    author_email="your.email@example.com",
    url="https://github.com/ProcheRAR/SwwwGUI",
    packages=find_namespace_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'PyGObject>=3.42.0',
    ],
    entry_points={
        'console_scripts': [
            'swwwgui=swww_gui.application:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment :: Window Managers",
    ],
    license="GPL-3.0",
    python_requires='>=3.8',
) 