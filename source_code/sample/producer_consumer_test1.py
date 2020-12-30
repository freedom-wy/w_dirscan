from queue import Queue
from concurrent.futures.thread import ThreadPoolExecutor
import random
import threading
import time

end_flag = object()


class Producer(threading.Thread):
    """生产者"""

    def __init__(self, task_queue, name=None):
        super().__init__(name=name)
        self._task_q = task_queue

    def run(self):
        for i in range(100):
            print("生产:", i)
            self._task_q.put(i)
        self._task_q.put(end_flag)


class Consumer(threading.Thread):
    """消费者"""

    def __init__(self, task_queue, name=None):
        super().__init__(name=name)
        self._task_q = task_queue

    def run(self):
        while True:
            result = self._task_q.get()
            # time.sleep(random.random())
            if result is end_flag:
                # 用于结束其他线程
                self._task_q.put(end_flag)
                break
            else:
                print("{thread_name}消费{value}".format(thread_name=threading.current_thread().name, value=result))


def main():
    c_list = []
    task_queue = Queue()
    p_list = [Producer(task_queue=task_queue, name="生产者")]
    for i in range(3):
        c_list.append(Consumer(task_queue=task_queue))

    for p in p_list:
        p.start()
    for c in c_list:
        c.start()

    for j_p in p_list:
        j_p.join()
    for j_c in c_list:
        j_c.join()
    print("队列剩余", task_queue.qsize())


if __name__ == '__main__':
    main()
