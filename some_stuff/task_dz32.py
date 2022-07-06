import os
import random
import string
import threading
import time
from multiprocessing.pool import ThreadPool

import requests


class timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return None

    def __exit__(self, type, value, traceback):
        elapsed_time = time.time() - self.start
        print(self.message.format(elapsed_time))


# 1. Потоки.


# def fetch_pic(num_pic):
#     url = "https://picsum.photos/400/600"
#     path = os.path.join(os.getcwd(), "img")
#     for _ in range(num_pic):
#         random_name = "".join(random.choices(string.ascii_letters + string.digits, k=5))
#         response = requests.get(url)
#         if response.status_code == 200:
#             with open(f"{path}/{random_name}.jpg", "wb") as f:
#                 f.write(response.content)
#
#
# workers = 200
# DATA_SIZE = 100
#
# with timer("Elapsed {}s"):
#     with ThreadPool(workers) as pool:
#         input_data = [DATA_SIZE // workers for _ in range(workers)]
#         pool.map(fetch_pic, input_data)

# # 2. Процеси.

DATA_SIZE = 1_000_000
lst = []


def fill_data(n):
    while n > 0:
        n -= 1
        lst.append(random.randint(1, 100))


# with timer("Elapsed {}s"):
#     fill_data(DATA_SIZE)

with timer("Elapsed {}s"):
    t1 = threading.Thread(target=fill_data, args=(DATA_SIZE // 1,))
    # t2 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))
    # t3 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))
    # t4 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))
    # t5 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))
    # t6 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))
    # t7 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))
    # t8 = threading.Thread(target=fill_data, args=(DATA_SIZE // 8,))

    t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    # t7.start()
    # t8.start()

    t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    # t6.join()
    # t7.join()
    # t8.join()
