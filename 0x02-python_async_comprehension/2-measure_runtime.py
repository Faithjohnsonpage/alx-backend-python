#!/usr/bin/env python3
"""This module implements a coroutine"""
import asyncio
import random
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """This coroutine that executes async_comprehension four times in
    parallel using asyncio.gather."""
    start_time = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    end_time = time.perf_counter() - start_time
    return end_time
