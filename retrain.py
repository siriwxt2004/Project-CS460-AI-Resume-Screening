import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def retrain_model():

    # โหลด dataset
    df = pd.read_csv(
        "data/feedback.csv"
    )

    # รวม text
    df["text"] = (
        df["jd"] + " " + df["resume"]
    )

    # train data
    X = df["text"]

    y = df["label"]

    # ML pipeline
    model = Pipeline([

        (
            "tfidf",

            TfidfVectorizer(
                max_features=3000
            )
        ),

        (
            "clf",

            LogisticRegression(
                max_iter=1000
            )
        )

    ])

    # train
    model.fit(X, y)

    # save model
    joblib.dump(
        model,
        "models/hr_model.pkl"
    )

    print("✅ retrained")