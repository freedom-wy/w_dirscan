import aiohttp
import asyncio


async def fetch(session, url):
    print("发送请求: ", url)
    async with session.get(url, verify_ssl=False) as response:
        text = await response.text()
        print(text)


async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            "https://www.baidu.com",
            "https://python.org"
        ]
        tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]
        done, pending = await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
