# beamwax

Comparing Beam and Bytewax

### Beam

Setup

```
python -m venv venv
source venv/bin/activate
pip install -r beam-requirements.txt
```

`beam-wordcount.py` just makes sure that everything is running. Then, we can create
a fake `parquet` file by running `python generate-parquet.py`. This file, `df.parquet`
contains a list of `user_ids` and their features.

`beam-parquet-proto.py` uses Beam to scan this file (in reality we should use Kafka
and stream) and tries to convert each row to a `protobuf` which, with a given
probability `p` (default `0`), is a wrong schema (`-c proto`) or a wrong field (`-c field`).
Unfortunately, this conversion is not done directly (`parquet` to `proto`), but uses an
intermediate JSON conversion, which can be a problem for some (complex) data types.

### Bytewax

Some dependencies are clashing with each other, so I just created a new virtual
environment.

```
python -m venv venv
source venv/bin/activate
pip install -r bw-requirements.txt
```

`bw-wordcount.py` implements the same wordcount, but uses `reduce_window` instead. A
`reduce` method is also available, but I haven't found a way to tell it when it stop...
But in a streaming case we need a window anyway.

`bw-parquet-proto.py` is basically a 1:1 translation of `beam-parquet-proto.py`: we can see it's a lot more "manual"
than Beam, everything needs to be specified, and again we use `reduce_window` to count
