#!/usr/bin/env python3
"""This module implements an asynchronous coroutine"""
import asyncio
import time
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Regular function that returns an asyncio.Task for
    wait_random(max_delay)"""
    return asyncio.create_task(wait_random(max_delay))
