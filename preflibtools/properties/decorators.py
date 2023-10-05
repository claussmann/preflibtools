"""This module contains decorators and exceptions which can be used for voting
rules and other functions, to ensure the input instance works for the function.
"""

from . import *
from preflibtools.instances.preflibinstance import *


class PreferenceIncompatibleError(Exception):
    pass


def requires_strict_preference(fn):
    def checker_fn(instance, *params):
        if not is_strict(instance):
            raise PreferenceIncompatibleError("Only strict preferences accepted.")
        return fn(instance, *params)
    return checker_fn


def requires_approval_preference(fn):
    def checker_fn(instance, *params):
        if not is_approval(instance):
            raise PreferenceIncompatibleError("Only approval preferences accepted.")
        return fn(instance, *params)
    return checker_fn


def requires_complete_preference(fn):
    def checker_fn(instance, *params):
        if not is_complete(instance):
            raise PreferenceIncompatibleError("Only complete preferences accepted.")
        return fn(instance, *params)
    return checker_fn


def requires_ordinal_preference(fn):
    def checker_fn(instance, *params):
        if not isinstance(instance, OrdinalInstance):
            raise PreferenceIncompatibleError("Only ordinal preferences accepted.")
        return fn(instance, *params)
    return checker_fn