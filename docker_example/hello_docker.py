import pandas as pd

import datetime
from time import sleep

print("Hello from docker!!!")

while True:
    # print(datetime.datetime.now())
    df = pd.DataFrame(
        data={
            "timestamp": [
                datetime.datetime.now(),
                datetime.datetime.now() + datetime.timedelta(days=7)
            ],
            "col2": [3, 4]
        }
    )
    sleep(2)
