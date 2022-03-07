'''
If an operation is io-bound and io is very slow, use asyncio.
If an operation is just io-bound, use threads.
if an operation is CPU bound, use multiprocessing.

buy, beg, build
'''
import asyncio


# Regular function.
def foo():
    return 1


# Async function.
async def bar():
    return 2


async def hello_async():
    print("hello async")

#asyncio.run(hello_async())







