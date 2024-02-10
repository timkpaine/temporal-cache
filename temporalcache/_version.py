# *****************************************************************************
#
# Copyright (c) 2021, the temporal-cache authors.
#
# This file is part of the temporal-cache library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", ["major", "minor", "micro", "releaselevel", "serial"])

# DO NOT EDIT THIS DIRECTLY!  It is managed by bumpversion
version_info = VersionInfo(0, 1, 5, "final", 0)

_specifier_ = {"alpha": "a", "beta": "b", "candidate": "rc", "final": ""}

__version__ = "{}.{}.{}{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    (
        ""
        if version_info.releaselevel == "final"
        else _specifier_[version_info.releaselevel] + "." + str(version_info.serial)
    ),
)
