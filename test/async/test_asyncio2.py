import time
import asyncio
import aiohttp
import pytest
from loguru import logger

# --- Asynchronous Functions (Legacy asyncio Style) ---

@asyncio.coroutine
def call_test_api_async(session, item_id: int):
    """Asynchronously calls the test API using legacy asyncio style.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        item_id (int): The ID of the item to request.

    Returns:
        dict or None: The JSON response from the API as a dictionary,
                      or None if an error occurred.
    """
    url = f"http://jpgcp.shop/pyapi/async/test/{item_id}"
    logger.info(f"Async call for item_id: {item_id}")
    try:
        response = yield from session.get(url)
        data = yield from response.json()
        logger.info(f"Async API response for item_id {item_id}: {data}")
        response.close()
        return data
    except aiohttp.ClientError as e:
        logger.error(f"Async API call for item_id {item_id} failed: {e}")
        return None

@asyncio.coroutine
def async_func1(session):
    """Async wrapper to call the API for item_id 1.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.

    Returns:
        dict or None: The result from the API call.
    """
    logger.info("async step 1")
    # `yield from` 将控制权交给事件循环来执行异步任务，是现代 `await` 关键字的前身。
    result = yield from call_test_api_async(session, 1)
    logger.info("async step 2")
    return result

@asyncio.coroutine
def async_func2(session):
    """Async wrapper to call the API for item_id 2.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.

    Returns:
        dict or None: The result from the API call.
    """
    logger.info("async step 3")
    # `yield from` 将控制权交给事件循环来执行异步任务，是现代 `await` 关键字的前身。
    result = yield from call_test_api_async(session, 2)
    logger.info("async step 4")
    return result

@pytest.mark.asyncio
@asyncio.coroutine
def test_asyncio():
    """Runs and times the asynchronous API calls concurrently."""
    logger.info("--- Starting Asynchronous Test (Legacy Style) ---")
    time_start = time.time()
    
    session = aiohttp.ClientSession()
    tasks = [
        async_func1(session),
        async_func2(session),
    ]
    results = yield from asyncio.gather(*tasks)
    yield from session.close()
    
    time_end = time.time()
    logger.info(f"All async tasks completed in {time_end - time_start:.2f} seconds")
    logger.info(f"Async API results: {results}")
    logger.info("--- Asynchronous Test (Legacy Style) Finished ---")
