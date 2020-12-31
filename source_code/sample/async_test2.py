import asyncio


# 定义了一个协程函数
# await后面接可等待对象，包括协程对象，future，task对象，IO等待
async def func1():
    print("test1")
    await asyncio.sleep(1)
    return "返回值"


async def main():
    print("main开始")
    task_list = [
        asyncio.create_task(func1()),
        asyncio.create_task(func1())
    ]
    print("main结束")
    done, pending = await asyncio.wait(task_list)
    print(done)
# 创建协程对象时，协程对象内部代码不会执行，需要将协程对象和事件循环搭配后才会执行协程内部代码
# asyncio.create_task()是在python3.7之后引入的，在python3.7之前使用asyncio.ensure_future方法
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
