import json
import os

DATASET_PATH = "data/feedback.jsonl"

def save_feedback(
    jd,
    resume,
    score,
    label
):

    os.makedirs(
        "data",
        exist_ok=True
    )

    row = {

        "jd": jd,

        "resume": resume,

        "score": score,

        "label": label

    }

    with open(
        DATASET_PATH,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(

            json.dumps(
                row,
                ensure_ascii=False
            )

            + "\n"

        )