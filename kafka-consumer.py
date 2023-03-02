from kafka import KafkaConsumer
from json import loads
from time import sleep

import user_pb2

consumer = KafkaConsumer(
    "topic_test",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group-id",
    value_deserializer=user_pb2.User.FromString,
)
for event in consumer:
    event_data = event.value
    print(event_data)
