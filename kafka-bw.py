import json
import os
import requests

import user_pb2

from datetime import timedelta

from bytewax.dataflow import Dataflow
from bytewax.execution import run_main
from bytewax.inputs import KafkaInputConfig
from bytewax.outputs import StdOutputConfig
from bytewax.window import SystemClockConfig, TumblingWindowConfig
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


clock_config = SystemClockConfig()
window_config = TumblingWindowConfig(length=timedelta(seconds=1))


def deserialize_proto(p):
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


def notify_on_slack(topic, reason):
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":safety_vest: Hydro anomaly detected",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"The `{topic}` topic is unhealthy. Reason: `{reason}`",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Learn more", "emoji": True},
                },
            },
        ]
    }
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json.dumps(payload))
    else:
        print("No webhook URL set, skipping Slack notification")


def count_per_key(count, event_count):
    return count + event_count


def super_complex_anomaly_detection(x):
    print(x)
    reason, value = x
    if reason != "Validated" and value > 3:
        print("Alert!")
        notify_on_slack("topic_test", reason)
    return x


flow = Dataflow()
flow.input("inp", KafkaInputConfig(["localhost:9092"], "topic_test", True, "end"))
flow.map(lambda x: (deserialize_proto(x[1]), 1))
flow.reduce_window("sum", clock_config, window_config, count_per_key)
flow.map(super_complex_anomaly_detection)
flow.capture(StdOutputConfig())

if __name__ == "__main__":
    run_main(flow)
