import pandas as pd
import json

rows = []

with open(
    "data/feedback.jsonl",
    encoding="utf-8"
) as f:

    for line in f:

        rows.append(
            json.loads(line)
        )

df = pd.DataFrame(rows)

df.to_csv(

    "data/feedback.csv",

    index=False,

    encoding="utf-8-sig"

)

print(df.head())