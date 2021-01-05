import aiohttp
import asyncio

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}


async def main():
    async with aiohttp.ClientSession() as session:
        # 发送一个GET请求
        # params = {"key1": "value1", "key2": "value2"}
        # async with session.get("http://httpbin.org/get", headers=headers, params=params) as response:
        # 发送一个Post请求
        # data = {
        #     "post": "test1"
        # }
        # async with session.post(url="http://httpbin.org/post", data=data) as response:
        # 下载图片
        # async with session.get(url="https://pic1.zhimg.com/v2-0a1dca7d906cec5d3f79743f50892625_1440w.jpg") as response:
        #     print(response.status)
        #     with open("test.jpg", "wb") as f:
        #         while True:
        #             jpg = await response.content.read(10)
        #             if not jpg:
        #                 break
        #             f.write(jpg)
        # 自定义cookie
        cookies = {"cookies_are": "working"}
        # async with session.get(url="http://httpbin.org/cookies", cookies=cookies) as response:
        response = await session.get(url="http://httpbin.org/cookies")
        print(await response.text())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
