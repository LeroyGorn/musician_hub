import asyncio


async def calculate(a):
    return a**a


async def test1():
    task = asyncio.create_task(calculate(11111))
    await task
    print("done!")


async def dots_printer():
    for i in range(100):
        print(".", end="")


async def test2():
    task = asyncio.create_task(dots_printer())
    await task
    print("done!")


async def test3():
    future = asyncio.Future()
    task = asyncio.create_task(set_future(future))
    await task
    print("done!")


async def test4():
    future = asyncio.Future()
    task = asyncio.create_task(wait_for_future(future))
    await task
    print("done!")


async def set_future(future):
    print("Future set result..")
    future.set_result(10)


async def wait_for_future(future):
    result = await future
    print("Future set result {}".format(result))


async def main():
    await asyncio.gather(test1(), test2(), test3(), test4())


asyncio.run(main())
