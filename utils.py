import argparse
import numpy as np

from google.protobuf import json_format

import user_bad_field_pb2
import user_pb2

parser = argparse.ArgumentParser(
    description="Just an example",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-p", "--prob", type=float, help="Probability of bad schema", default=0
)
parser.add_argument(
    "-c", "--change", type=str, help="What to change", default=0
)


args = parser.parse_args()
config = vars(args)

if config["prob"] < 0 or config["prob"] > 1:
    raise ValueError("Probability must be between 0 and 1")

if not config["change"]:
    config["change"] = 'proto'


def TryCastAsProto(message):
    # Unfortunately we have to pass through JSON. Maybe in Java there are better ways!
    # Not sure we can use schemas in Beam:  
    # https://beam.apache.org/documentation/programming-guide/#creating-schemas
    change = np.random.random() < config["prob"]

    user = user_pb2.User()

    if change:
        if config["change"] == 'proto':
            user = user_bad_field_pb2.UserBad()
        elif config["change"] == 'field':
            # Change field from string to integer
            message['user_id'] = np.random.randint(0, 100000)

    try:
        print(message)        
        json_format.ParseDict(message, user)
    except json_format.ParseError:
        return "Bad schema"
    return "Good schema"