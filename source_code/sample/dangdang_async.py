import asyncio
import aiohttp
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}


async def handle_request(session, url):
    """异步请求方法"""
    print(url)
    async with session.get(url=url, headers=headers, verify_ssl=False) as response:
        if response.status == 200:
            text = await response.text(errors="ignore")
            # await handle_response(text)


async def handle_response(text):
    """异步解析方法"""
    html = etree.HTML(text)
    items = html.xpath("//ul[@class='bang_list']/li")
    for item in items:
        title = item.xpath(".//div[@class='name']/a/text()")
        if title:
            print(title[0])


async def main(url_list):
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            await handle_request(session, url)
        # tasks = [asyncio.create_task(handle_request(session, url)) for url in url_list]
        # await asyncio.wait(tasks)


if __name__ == '__main__':
    url_list = ["http://bang.dangdang.com/books/fivestars/2-{url}".format(url=url) for url in range(1, 26)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url_list))
