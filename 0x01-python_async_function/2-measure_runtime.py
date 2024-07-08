#!/usr/bin/env python3
"""This module implements an asynchronous coroutine"""
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


async def async_measure_time(n: int, max_delay: int) -> float:
    """This measures the total execution time for wait_n(n, max_delay),
    and returns total_time / n."""
    start_time = time.perf_counter()
    await wait_n(n, max_delay)
    total_time = time.perf_counter() - start_time
    return total_time / n


def measure_time(n: int, max_delay: int) -> float:
    """Synchronous wrapper to measure the total execution time for
    wait_n(n, max_delay) and return total_time / n."""
    return asyncio.run(async_measure_time(n, max_delay))
