import numpy as np
import random
import time
import uuid
import user_pb2

from datetime import timedelta

from bytewax.dataflow import Dataflow
from bytewax.execution import run_main
from bytewax.inputs import ManualInputConfig
from bytewax.outputs import StdOutputConfig
from bytewax.window import SystemClockConfig, TumblingWindowConfig


def random_datapoints(worker_index, worker_count, state):
    state = None
    for i in range(1000):
        time.sleep(0.1)
        u = user_pb2.User()
        u.user_id = str(uuid.uuid4())
        u.feature = chr(ord("a") + np.random.randint(0, 26))

        change = np.random.random() < 0.1

        if change:
            # Delete one field
            u.ClearField("feature")

        yield state, u


clock_config = SystemClockConfig()
window_config = TumblingWindowConfig(length=timedelta(seconds=1))


flow = Dataflow()
flow.input("inp", ManualInputConfig(random_datapoints))
flow.map(lambda x: ("present" if x.HasField("feature") else "not_present", 1))
flow.reduce_window("sum", clock_config, window_config, lambda x, s: x + s)
flow.capture(StdOutputConfig())

if __name__ == "__main__":
    run_main(flow)
