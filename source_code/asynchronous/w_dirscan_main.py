from fake_useragent import UserAgent
import asyncio
import aiohttp
import time
import os
import threading
import sys
import json
from queue import Queue
from urllib.parse import urlparse
from argparse import ArgumentParser

# 队列停止符
end_flag = object()
# 循环结束
end_while = False


class HandleRequest(object):
    def __init__(self, ua, status_code, proxy, timeout, retry):
        self.proxy = proxy
        self.timeout = timeout
        self.retry = retry
        self.status_code = status_code
        self.ua = ua

    async def do_request(self, session, url):
        """发送请求"""
        header = {
            "User-Agent": self.ua.random
        }
        for i in range(self.retry):
            try:
                async with session.get(url, headers=header, verify_ssl=False, timeout=self.timeout) as response:
                    if response and response.status == 200:
                        print(url + "\n")
                        break
            except Exception as e:
                continue


class Getdir(threading.Thread):
    def __init__(self, task_queue, input_item):
        super().__init__()
        self._task_q = task_queue
        # 获取字典列表
        self.file_list = get_all_file(input_item)

    def run(self):
        for file in self.file_list:
            # 读取字典
            with open(file, "r", encoding="utf-8") as f:
                while True:
                    try:
                        buffer = f.readline()
                    except UnicodeDecodeError:
                        continue
                    if not buffer:
                        break
                    result = buffer.split("\n")[0]
                    # 放入目录数据
                    self._task_q.put(result)
        # 放入停止符
        self._task_q.put(end_flag)


def get_all_file(input_item):
    """获取字典列表"""
    if not input_item:
        default_file = ["DIR.txt"]
        file_list = [os.path.join("yujian_dictionary", item) for item in default_file]
    else:
        file_list = [os.path.join("yujian_dictionary", item) for item in input_item]
    return file_list


def handle_url_dir(url, dir_path):
    # 判断目录有没有/
    if not dir_path.startswith("/"):
        dir_path = "{}{}".format("/", dir_path)
    url_info = urlparse(url)
    # 判断协议
    if not url_info.scheme:
        url = "http://{_url}".format(_url=url)
    # # 判断URL结尾有没有/
    if url_info.path == "/":
        url = url.rstrip("/")
    request_url = "{_url}{_dir}".format(_url=url, _dir=dir_path)
    return request_url


async def schedule(url, queue, status_code, proxy, timeout, retry, thread_pool):
    """调度方法"""
    global end_while
    # 随机UA
    ua = UserAgent()
    # 使用协程发送请求
    h = HandleRequest(ua=ua, status_code=status_code, proxy=proxy, timeout=timeout, retry=retry)
    async with aiohttp.ClientSession() as session:
        while not end_while:
            url_list = []
            for i in range(thread_pool):
                dir_path = queue.get()
                if dir_path is end_flag:
                    end_while = True
                    break
                else:
                    request_url = handle_url_dir(url, dir_path=dir_path)
                    url_list.append(request_url)
            # 协程
            tasks = [asyncio.create_task(h.do_request(session, url)) for url in url_list]
            await asyncio.wait(tasks)


def main(url, dictionary_list):
    q = Queue()
    # 生产者
    g = Getdir(task_queue=q, input_item=dictionary_list)
    # 线程启动
    g.start()
    # 读取配置文件
    with open("config.json", "r", encoding="utf-8") as f:
        f = json.loads(f.read())
    # 获取配置文件配置项
    config = f.get("config_item")
    status_code = config.get("status_code")
    proxy = config.get("proxy")
    if proxy:
        proxy = {
            "http": proxy,
            "https": proxy
        }
    timeout = config.get("timeout")
    retry = config.get("retry")
    thread_pool = config.get("thread_pool")
    # 如果未设置配置文件，将使用默认参数
    if not all([status_code, timeout, retry, thread_pool]):
        status_code = [200]
        timeout = 3
        retry = 1
        thread_pool = 20
    # 消费者
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schedule(url=url, queue=q, status_code=status_code, proxy=proxy, timeout=timeout, retry=retry, thread_pool=thread_pool))
    g.join()


if __name__ == '__main__':
    dictionary_list = []
    parser = ArgumentParser(prog="W_DIRSCAN", usage="基于御剑字典的目录扫描", epilog="微信公众号:你丫才秃头")
    parser.add_argument("URL", help="扫描的URL或IP地址")
    parser.add_argument("-a", "--asp", dest="asp", action="store_true", help="加载asp,aspx字典")
    parser.add_argument("-d", "--dir", dest="dir", action="store_true", help="加载dir字典")
    parser.add_argument("-j", "--jsp", dest="jsp", action="store_true", help="加载jsp字典")
    parser.add_argument("-m", "--mdb", dest="mdb", action="store_true", help="加载mdb字典")
    parser.add_argument("-p", "--php", dest="php", action="store_true", help="加载php字典")
    parser.add_argument("--all", dest="all", action="store_true", help="加载所有字典")
    args = parser.parse_args()
    url = sys.argv[1]
    if args.all and (args.asp or args.dir or args.jsp or args.mdb or args.php):
        print("不能同时使用--all参数和其他单独参数")
        sys.exit(1)
    if args.asp:
        dictionary_list.extend(["ASP.TXT", "ASPX.TXT"])
    if args.dir:
        dictionary_list.extend(["DIR.TXT"])
    if args.jsp:
        dictionary_list.extend(["JSP.TXT"])
    if args.mdb:
        dictionary_list.extend(["MDB.TXT"])
    if args.php:
        dictionary_list.extend(["PHP.TXT"])
    if args.all:
        dictionary_list.extend(["ASP.TXT", "ASPX.TXT", "DIR.TXT", "JSP.TXT", "MDB.TXT", "PHP.TXT"])


    def handle_time():
        """处理时间"""
        timestamp = time.time()
        time_local = time.localtime(timestamp)
        time_format = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return timestamp, time_format


    start_timestamp, start_time = handle_time()
    print("开始扫描时间{}".format(start_time))
    # 调用主方法
    main(url=url, dictionary_list=dictionary_list)
    end_timestamp, end_time = handle_time()
    print("扫描完成时间{}, 扫描耗时:{}分钟".format(end_time, int((end_timestamp - start_timestamp) / 60)))
