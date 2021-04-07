# -*- coding: utf-8 -*-

"""
seamm_default_atomtyping
A plug-in that implements the default atomtyping method in SEAMM
"""

# Bring up the classes so that they appear to be directly in
# the seamm_default_atomtyping package.

from seamm_default_atomtyping.seamm_default_atomt import SeammDefaultAtomtyping  # noqa: F401, E501
from seamm_default_atomtyping.seamm_default_atomt_parameters import SeammDefaultAtomtypingParameters  # noqa: F401, E501
from seamm_default_atomtyping.seamm_default_atomt_step import SeammDefaultAtomtypingStep  # noqa: F401, E501
from seamm_default_atomtyping.tk_seamm_default_atomt import TkSeammDefaultAtomtyping  # noqa: F401, E501

# Handle versioneer
from ._version import get_versions
__author__ = """Eliseo Marin"""
__email__ = 'meliseo@vt.edu'
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
