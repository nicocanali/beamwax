import apache_beam as beam

import utils


with beam.Pipeline() as pipeline:
    data = pipeline | beam.io.ReadFromParquet("df.parquet")
    (
        data
        | "Convert to proto via JSON" >> beam.Map(utils.TryCastAsProto)
        | beam.combiners.Count.PerElement()
        | beam.Map(print)
    )
