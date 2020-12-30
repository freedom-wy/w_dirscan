from fake_useragent import UserAgent
import time
import os
import threading
from concurrent.futures.thread import ThreadPoolExecutor
import requests
import json
from queue import Queue
from urllib.parse import urlparse

# 队列停止符
end_flag = object()


class HandleRequest(object):
    def __init__(self, ua, status_code, proxy, timeout, retry):
        self.proxy = proxy
        self.timeout = timeout
        self.retry = retry
        self.status_code = status_code
        self.ua = ua

    def do_request(self, url):
        """发送请求"""
        header = {
            "User-Agent": self.ua.random
        }
        for i in range(self.retry):
            try:
                response = requests.get(url=url, headers=header, proxies=self.proxy, timeout=self.timeout)
            except Exception as e:
                # print(e)
                continue
            else:
                if response and response.status_code in self.status_code:
                    print(url + "\n")
                    break


class Getdir(threading.Thread):
    def __init__(self, task_queue, input_item):
        super().__init__()
        self._task_q = task_queue
        self.file_list = get_all_file(input_item)

    def run(self):
        for file in self.file_list:
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
    file_list = []
    if not input_item:
        # default_file = ["dir.txt", "main.txt"]
        default_file = ["DIR.txt"]
        file_list = [os.path.join("yujian_dictionary", item) for item in default_file]
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


def schedule(url, queue, status_code, proxy, timeout, retry, thread_pool):
    """调度方法"""
    ua = UserAgent()
    # 使用线程池发送请求
    h = HandleRequest(ua=ua, status_code=status_code, proxy=proxy, timeout=timeout, retry=retry)
    with ThreadPoolExecutor(thread_pool) as pool:
        while True:
            dir = queue.get()
            if dir is end_flag:
                queue.put(end_flag)
                break
            else:
                request_url = handle_url_dir(url, dir_path=dir)
                # print(request_url)
            pool.submit(h.do_request, request_url)


def main(url):
    q = Queue()
    g = Getdir(task_queue=q, input_item=None)
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
    if not all([status_code, timeout, retry, thread_pool]):
        status_code = [200]
        timeout = (3, 3)
        retry = 3
        thread_pool = 30
    schedule(url=url, queue=q, status_code=status_code, proxy=proxy, timeout=timeout, retry=retry,
             thread_pool=thread_pool)
    g.join()


if __name__ == '__main__':
    start_time = time.time()
    main(url="http://192.168.52.143")
    print(time.time()-start_time)
