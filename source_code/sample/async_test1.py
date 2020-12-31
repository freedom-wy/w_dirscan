import asyncio


# 定义一个协程方法
async def func1():
    print(1)
    # 遇到网络IO请求
    await asyncio.sleep(1)
    print(2)


async def func2():
    print(3)
    await asyncio.sleep(1)
    print(4)

task = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))
