import src.configs.config
import aiohttp
import asyncio
from loguru import logger
import time
import pytest

# --- Asynchronous Functions (Modern async/await Style) ---

async def call_test_api_modern_async(session, item_id: int):
    """Asynchronously calls the test API using modern async/await syntax."""
    url = f"http://jpgcp.shop/pyapi/async/test/{item_id}"
    logger.info(f"Modern async call for item_id: {item_id}")
    try:
        # 使用 async with 确保 session 和 response 被正确管理
        async with session.get(url) as response:
            # await 替代了 yield from
            data = await response.json()
            logger.info(f"Modern async API response for item_id {item_id}: {data}")
            return data
    except aiohttp.ClientError as e:
        logger.error(f"Modern async API call for item_id {item_id} failed: {e}")
        return None

async def async_func1_modern(session):
    """Modern async wrapper to call the API for item_id 1."""
    logger.info("modern async step 1")
    # await 替代了 yield from
    result = await call_test_api_modern_async(session, 1)
    logger.info("modern async step 2")
    return result

async def async_func2_modern(session):
    """Modern async wrapper to call the API for item_id 2."""
    logger.info("modern async step 3")
    # await 替代了 yield from
    result = await call_test_api_modern_async(session, 2)
    logger.info("modern async step 4")
    return result

@pytest.mark.asyncio
async def test_modern_asyncio():
    """Runs and times the modern asynchronous API calls concurrently."""
    logger.info("--- Starting Asynchronous Test (Modern Style) ---")
    time_start = time.time()
    
    # 使用 async with 自动管理 session 的生命周期
    async with aiohttp.ClientSession() as session:
        tasks = [
            async_func1_modern(session),
            async_func2_modern(session),
        ]
        # await 替代了 yield from
        results = await asyncio.gather(*tasks)
    
    time_end = time.time()
    logger.info(f"All modern async tasks completed in {time_end - time_start:.2f} seconds")
    logger.info(f"Modern async API results: {results}")
    logger.info("--- Asynchronous Test (Modern Style) Finished ---")
