import numpy as np
import random
import time
import uuid
import user_pb2

from datetime import timedelta

from bytewax.dataflow import Dataflow
from bytewax.execution import run_main
from bytewax.inputs import KafkaInputConfig
from bytewax.outputs import StdOutputConfig
from bytewax.window import SystemClockConfig, TumblingWindowConfig


clock_config = SystemClockConfig()
window_config = TumblingWindowConfig(length=timedelta(seconds=1))


def DeserializeProto(p):
    try:
        u = user_pb2.User.FromString(p)

        # Checks
        if not u.user_id:
            return "User ID is missing"

        if not u.HasField("feature_enum"):
            return "Missing field"

        if u.feature_enum == user_pb2.Feature.FEATURE_UNKNOWN:
            return "Unknown value"

        return "Validated"
    except:
        # If the message can't be deserialized, also return bad schema
        return "Bad schema"


flow = Dataflow()
flow.input("inp", KafkaInputConfig(["localhost:9092"], "topic_test", True, "beginning"))
flow.map(lambda x: (DeserializeProto(x[1]), 1))
flow.reduce_window("sum", clock_config, window_config, lambda x, s: x + s)
flow.capture(StdOutputConfig())

if __name__ == "__main__":
    run_main(flow)
