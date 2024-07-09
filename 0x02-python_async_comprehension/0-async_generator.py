#!/usr/bin/env python3
"""This module implements a coroutine"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """This coroutine loops 10 times, each time asynchronously wait 1 second,
    then yield a random number between 0 and 10."""
    loop = 10
    while loop:
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
        loop -= 1
