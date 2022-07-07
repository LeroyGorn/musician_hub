import asyncio


async def calculate(a):
    return a**a


async def dots_printer():
    for i in range(100):
        print(".", end="")


async def stop_event_loop(loop):
    loop.stop()
    print("Endloop")


async def set_future(future):
    print("Future set result..")
    future.set_result(10)


async def wait_for_future(future):
    result = await future
    print("Future set result {}".format(result))


event_loop = asyncio.get_event_loop()
fut = asyncio.Future()
event_loop.create_task(dots_printer())

event_loop.create_task(calculate(11111))

event_loop.create_task(set_future(fut))

event_loop.create_task(wait_for_future(fut))

event_loop.run_forever()
event_loop.close()
