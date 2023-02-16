# beamwax
Comparing Beam and Bytewax

### Beam

Setup

```
python -m venv beamenv
source beamenv/bin/activate
pip install -r beam-requirements.txt
```

`beam-wordcount.py` just makes sure that everything is running. Then, we can create
a fake `parquet` file by running `python beam-parquet.py`. This file, `df.parquet` 
contains a list of `user_ids` and their features.

`beam-parquet-proto.py` uses Beam to scan this file (in reality we should use Kafka)
and tries to convert each row to a `protobuf` which, with a given probability `p`, is a
wrong schema. Unfortunately, this conversion is not done directly (`parquet` to `proto`),
but uses an intermediate JSON conversion, which can be a problem for some (complex)
data types.