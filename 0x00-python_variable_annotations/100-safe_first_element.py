#!/usr/bin/env python3
"""This module implements a type-annotated function"""
from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Return the first element of the list if it exists, otherwise None."""
    if lst:
        return lst[0]
    else:
        return None
