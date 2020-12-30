import time
import queue

import threading
import random

# 哨兵
_sentinel = object()


class Producer(threading.Thread):
    """
    只负责产生数据
    """

    def __init__(self, name, queue):
        # python3的写法
        super().__init__(name=name)
        self.queue = queue

    def run(self):
        for i in range(15):
            print("%s is producing %d to the queue!" % (self.getName(), i))
            self.queue.put(i)
            # time.sleep(random.randint(1, 20) * 0.1)

        # 设置完成的标志位
        self.queue.put(_sentinel)
        print("%s finished!" % self.getName())


class Consumer(threading.Thread):
    """
    数据处理,对数据进行消费.
    """

    def __init__(self, name, queue):
        super().__init__(name=name)
        self.queue = queue

    def run(self):
        while True:
            value = self.queue.get()
            # 用来退出线程
            if value is _sentinel:
                # 添加哨兵,让其他线程有机会退出来
                self.queue.put(value)
                break
            else:
                print("{} is consuming. {} in the queue is consumed!".format(self.getName(), value))
                if value % 2 == 0:
                    value = value + random.randint(1, 3)
                    self.queue.put(value)

        print("%s finished!" % self.getName())


if __name__ == '__main__':
    queue = queue.Queue()
    producer = Producer('producer', queue)

    producer.start()

    consumer_threads = []
    for i in range(3):
        consumer = Consumer('consumer_' + str(i), queue)
        consumer_threads.append(consumer)
        consumer.start()

    producer.join()
    for consumer in consumer_threads:
        consumer.join()

    print(queue.qsize(), "11111111111111")
    # producer.join()

    print('All threads  done')
