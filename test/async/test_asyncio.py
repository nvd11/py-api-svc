import src.configs.config
from loguru import logger
import asyncio


async def func1():
    logger.info("step 1")    # Log step 1
    await asyncio.sleep(2)   # Asynchronously wait for 2 seconds
    logger.info("step 2")    # Log step 2


async def func2():
    logger.info("step 3")    # Log step 3
    await asyncio.sleep(2)   # Asynchronously wait for 2 seconds
    logger.info("step 4")    # Log step 4


async def test_asyncio():
    tasks = [                # Create a list of coroutine tasks
        func1(),
        func2(),
    ]
    await asyncio.gather(*tasks) # Run the tasks concurrently
 