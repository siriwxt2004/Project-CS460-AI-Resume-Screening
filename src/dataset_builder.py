import os
import pandas as pd


def save_feedback(
    jd,
    resume,
    score,
    label
):

    # สร้าง folder data ถ้ายังไม่มี
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

    csv_path = "data/feedback.csv"

    # ถ้ายังไม่มีไฟล์
    if not os.path.exists(csv_path):

        df = pd.DataFrame([row])

        df.to_csv(
            csv_path,
            index=False
        )

    else:

        df = pd.read_csv(csv_path)

        new_df = pd.concat(

            [
                df,
                pd.DataFrame([row])
            ],

            ignore_index=True

        )

        new_df.to_csv(
            csv_path,
            index=False
        )

    print("✅ feedback saved")