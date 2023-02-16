from datetime import timedelta

from bytewax.dataflow import Dataflow
from bytewax.execution import run_main
from bytewax.inputs import ManualInputConfig
from bytewax.outputs import StdOutputConfig
from bytewax.window import SystemClockConfig, TumblingWindowConfig

import pyarrow.parquet as pq

import utils


def input_builder(worker_index, worker_count, resume_state):
    state = None  # Ignore recovery
    t = pq.read_table('df.parquet')
    for batch in t.to_batches():
        batch_list = batch.to_pylist()
        for row in batch_list:
            yield (state, row)

clock_config = SystemClockConfig()
window_config = TumblingWindowConfig(length=timedelta(seconds=10))

def add(x, s):
    return x + s

flow = Dataflow()
flow.input("inp", ManualInputConfig(input_builder))
flow.map(utils.TryCastAsProto)
flow.map(lambda x: (x, 1))
flow.reduce_window("sum", clock_config, window_config, add)
flow.capture(StdOutputConfig())

run_main(flow)