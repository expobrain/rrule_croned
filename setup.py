#!/usr/bin/env python

from pathlib import Path
from setuptools import setup, find_namespace_packages

import os


# Get long_description from README.md
long_description = (Path(__file__).parent / "README.md").read_text().strip()

setup(
    name="rrule_croned",
    license="MIT",
    url="https://github.com/expobrain/rrule_croned",
    version="0.1.0",
    description="Converts recurrence rules into cron expressions",
    long_description=long_description,
    author="Daniele Esposti <daniele.esposti@gmail.com>",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=["dataclasses>=0.6", "python-dateutil>=2.8"],
)
