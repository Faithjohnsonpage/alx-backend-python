#!/usr/bin/env python3
"""This module implements an asynchronous coroutine"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """This async routine calls wait_n and spawns wait_random n
    times with the specified max_delay"""
    tasks = [wait_random(max_delay) for _ in range(n)]
    results = await asyncio.gather(*tasks)
    return results
