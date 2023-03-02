from json import dumps
from kafka import KafkaProducer
from time import sleep


import random
import uuid
import user_pb2


producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    key_serializer=lambda x: dumps(x).encode("utf-8"),
    value_serializer=lambda x: u.SerializeToString(),
)
for j in range(9999):
    print(j)
    u = user_pb2.User()
    u.user_id = str(uuid.uuid4())

    if random.random() < 0.5:
        feature = user_pb2.Feature.FEATURE_A
    else:
        feature = user_pb2.Feature.FEATURE_B

    u.feature_enum = feature

    if random.random() < 0.2:
        u.feature_enum = user_pb2.Feature.FEATURE_UNKNOWN

    if random.random() < 0.1:
        u.ClearField("feature_enum")

    if random.random() < 0.1:
        u.user_id = ""

    print(u)

    producer.send("topic_test", key=j, value=u)

    sleep(0.1)
