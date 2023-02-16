import os
import uuid

import numpy as np
import pandas as pd


# create a parquet file if it doesn't exist
if not os.path.exists("df.parquet"):
    # Create a ranom list of 100 unique user ids
    length = 100

    user_ids = [str(uuid.uuid4()) for _ in range(length)]
    # sample a random letter from the alphabet
    features = [chr(ord("a") + i) for i in np.random.randint(0, 26, size=length)]

    df = pd.DataFrame(data={"user_id": user_ids, "feature": features})
    df.to_parquet("df.parquet")
else:
    print("File already exists, skipping")
