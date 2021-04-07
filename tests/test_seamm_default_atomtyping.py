#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_default_atomtyping` package."""

import pytest  # noqa: F401
import seamm_default_atomtyping  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = seamm_default_atomtyping.SeammDefaultAtomtyping()
    assert str(type(result)) == (
        "<class 'seamm_default_atomtyping.seamm_default_atomt.SeammDefaultAtomtyping'>"  # noqa: E501
    )
