#!/usr/bin/env python3
"""This module implements a type-annotated function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """This function takes a float multiplier as an argument and returns
    a function that multiplies a float by the multiplier."""
    def multiplier_function(value: float) -> float:
        return multiplier * value
    return multiplier_function
