import threading

# 多进程修改值
value = []


def test1():
    # global value
    for i in range(1000000):
        # 使用锁解决多线程共享变量时的不安全问题
        # lock.acquire()
        value.append(i)
        result = value.pop()
        print(result)
        # lock.release()


def thread_value():
    t1 = threading.Thread(target=test1)
    t2 = threading.Thread(target=test1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    # 进程与进程之间不共享数据
    # multiprocess_value()
    # print(value)
    # 多线程间共享数据
    thread_value()
    print(value)
