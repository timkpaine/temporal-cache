# *****************************************************************************
#
# Copyright (c) 2021, the temporal-cache authors.
#
# This file is part of the temporal-cache library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import io
import os
import os.path
from codecs import open

from setuptools import find_packages, setup

name = "temporal-cache"
here = os.path.abspath(os.path.dirname(__file__))
pjoin = os.path.join


def get_version(file, name="__version__"):
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


version = get_version(pjoin(here, "temporalcache", "_version.py"))

with open(pjoin(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read().replace("\r\n", "\n")


requires = [
    "frozendict>=1.2",
    "tzlocal>=2.0.0",
]

requires_dev = [
    "black>=20",
    "bump2version>=1.0.0",
    "flake8>=3.7.8",
    "flake8-black>=0.2.1",
    "mock",
    "pytest>=4.3.0",
    "pytest-cov>=2.6.1",
    "Sphinx>=1.8.4",
    "sphinx-markdown-builder>=0.5.2",
] + requires


setup(
    name=name,
    version=version,
    description="Time based function caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timkpaine/{name}".format(name=name),
    author="Tim Paine",
    author_email="t.paine154@gmail.com",
    license="Apache 2.0",
    install_requires=requires,
    extras_require={
        "dev": requires_dev,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="analytics tools",
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    include_package_data=True,
    zip_safe=False,
)
