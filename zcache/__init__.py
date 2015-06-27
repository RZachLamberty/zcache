#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: __init__.py
Author: zlamberty
Created: 2015-06-16

Description:
    caching layer, stolen shamelessly from
    http://stackoverflow.com/questions/15585493/store-the-cache-to-a-file-functools-lru-cache-in-python-3-2

Usage:
    <usage>

"""

import collections
import logging
import logging.config
import os
import pickle

import constants


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

ACTIVE_CACHES = {}
logger = logging.getLogger(__name__)
logging.config.dictConfig(constants.LOGCONF)


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

class Cache(dict):
    global ACTIVE_CACHES
    def __init__(self, cachename, f=None):
        self.cachename = cachename
        ACTIVE_CACHES[self.cachename] = self
        self.f = f
        self.load_cache_from_file()

    def __del__(self):
        print('in actual cache object __del__')
        with open(self.f, 'wb') as fpkl:
            pickle.dump(self.copy(), fpkl)
        #self.save_cache()

    def load_cache_from_file(self):
        """ allow for a pickle file based cache """
        if self.f is None:
            pass
        else:
            try:
                with open(self.f, 'rb') as fpkl:
                    self.update(pickle.load(fpkl))
            except EOFError:
                logger.warning("cache file exists but is empty")
                pass
            except Exception as e:
                if os.access(self.f, os.R_OK):
                    err = "file {} exists but we were unable to unpickle it"
                    err = err.format(self.f)
                    logger.warning(err)
                else:
                    logger.warning("file {} not readable".format(self.f))

                logger.debug("error type: {}".format(type(e)))
                logger.debug("error message: {}".format(e))
                logger.debug("continuing with empty cache in its place")

    def save_cache(self):
        if self.f is None:
            logger.debug("no cache file, skipping save")
        else:
            with open(self.f, 'wb') as fpkl:
                pickle.dump(self.copy(), fpkl)


class cached(object):
    def __init__(self, cachename, f=None):
        self.f = f
        self.cachename = cachename
        self.cache = Cache(self.cachename, self.f)

    def __del__(self):
        print('in cached wrapper __del__')
        self.cache.save_cache()

    def __call__(self, func):
        def wrapped_func(*args):
            if not isinstance(args, collections.Hashable):
                return func(*args)
            if args in self.cache:
                return self.cache[args]
            else:
                self.cache[args] = value = func(*args)
                return value
        wrapped_func.cache = self.cache
        return wrapped_func
