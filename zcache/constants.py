#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: constants.py
Author: zlamberty
Created: 2015-06-08

Description:
    constants for the zcache module

Usage:
    <usage>

"""

import os
import yaml


FCONF = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'logging.yaml'
)
with open(FCONF, 'rb') as f:
    LOGCONF = yaml.load(f)
