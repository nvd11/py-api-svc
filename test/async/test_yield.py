import src.configs.config
from loguru import logger



def generator1():
    # First, the generator yields the value 1.
    yield 1
    # Then, it delegates execution to generator2.
    # 'yield from' iterates over generator2 and yields all its values (3, 4).
    yield from generator2()
    # After generator2 is exhausted, generator1 resumes and yields the value 2.
    yield 2
   

def generator2():
    # This generator first yields the value 3.
    yield 3
    # Then it yields the value 4.
    yield 4
    # will return to generator1 after this.



def test_yield():
    # Create a generator instance from generator1.
    gen = generator1()
    # Collect all yielded values from the generator into a list.
    # This will execute the generator to completion:
    # 1. Get 1 from generator1.
    # 2. 'yield from generator2' starts.
    # 3. Get 3 from generator2.
    # 4. Get 4 from generator2.
    # 5. 'yield from' finishes.
    # 6. Get 2 from generator1.
    # So, `results` will be [1, 3, 4, 2].
    results = list(gen)
    # Log the generated results.
    logger.info(f"Generator results: {results}")
    # Assert that the results list matches the expected sequence.
    assert results == [1, 3, 4, 2]
