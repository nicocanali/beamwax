import apache_beam as beam
import re

with beam.Pipeline() as pipeline:
    lines =  (
        pipeline
        | beam.Create([
            'To be, or not to be: that is the question: ',
            "Whether 'tis nobler in the mind to suffer ",
            'The slings and arrows of outrageous fortune, '
            'Or to take arms against a sea of troubles, ',
      ]))
    (
        lines
        | 'ExtractWords' >> beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
        | beam.Map(str.lower)
        | beam.combiners.Count.PerElement()
        | beam.Map(print)
    )
   
     