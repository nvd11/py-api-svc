import src.configs.config
from loguru import logger
import asyncio
import pytest

@asyncio.coroutine
def func1():
    logger.info("step 1")    # Log step 1
    yield from asyncio.sleep(2)   # Asynchronously wait for 2 seconds
    logger.info("step 2")    # Log step 2

@asyncio.coroutine
def func2():
    logger.info("step 3")    # Log step 3
    yield from asyncio.sleep(2)   # Asynchronously wait for 2 seconds
    logger.info("step 4")    # Log step 4

@pytest.mark.asyncio
@asyncio.coroutine
def test_asyncio():
    tasks = [                # Create a list of coroutine tasks
        func1(),
        func2(),
    ]
    yield from asyncio.gather(*tasks) # Run the tasks concurrently

# To make the file runnable for verification
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_asyncio())
