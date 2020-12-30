from queue import Queue
import threading


class Producer(threading.Thread):
    """生产者"""

    def __init__(self, task_queue, start, end, name=None):
        super().__init__(name=name)
        self._task_q = task_queue
        self.start_value = start
        self.end_value = end

    def run(self):
        for i in range(self.start_value, self.end_value):
            print("生产:", i)
            self._task_q.put(i)


class Consumer(threading.Thread):
    """消费者"""
    def __init__(self, task_queue, name=None):
        super().__init__(name=name)
        self._task_q = task_queue

    def run(self):
        while self._task_q.qsize() > 0:
            result = self._task_q.get()
            print("{thread_name}消费{value}".format(thread_name=threading.current_thread().name, value=result))


def main():
    task_queue = Queue()
    c_list = []
    # 生产者
    p_list = [Producer(task_queue=task_queue, start=0, end=10),
              Producer(task_queue=task_queue, start=10, end=20)]
    # 消费者
    for i in range(3):
        c_list.append(Consumer(task_queue=task_queue))

    for p in p_list:
        p.start()

    for c in c_list:
        c.start()

    for p in p_list:
        p.join()

    for c in c_list:
        c.join()


if __name__ == '__main__':
    main()
