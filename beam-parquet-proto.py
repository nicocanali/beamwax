import argparse

import apache_beam as beam
from google.protobuf import json_format
import numpy as np
import pyarrow as pa

import user_bad_field_pb2
import user_pb2


parser = argparse.ArgumentParser(
    description="Just an example",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-p", "--prob", type=float, help="Probability of bad schema", default=0
)

args = parser.parse_args()
config = vars(args)

if config["prob"] < 0 or config["prob"] > 1:
    raise ValueError("Probability must be between 0 and 1")


def TryCastAsProto(message):
    # Generate a random number between 0 and 1
    # If it's less than the probability, use the bad schema
    if np.random.random() < config["prob"]:
        user = user_bad_field_pb2.UserBad()
    else:
        user = user_pb2.User()

    try:
        json_format.ParseDict(message, user)
    except json_format.ParseError:
        return "Bad schema"
    return "Good schema"


with beam.Pipeline() as pipeline:
    data = pipeline | beam.io.ReadFromParquet("df.parquet")
    # fmt: off
    (

        data
        # Unfortunately we have to pass through JSON. Maybe in Java there are better ways!
        # Not sure we can use schemas in Beam: 
        # https://beam.apache.org/documentation/programming-guide/#creating-schemas
        | "Convert to proto via JSON" >> beam.Map(TryCastAsProto)
        | beam.combiners.Count.PerElement()
        | beam.Map(print)
    )
