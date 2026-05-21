import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import joblib

df = pd.read_csv(
    "data/feedback.csv"
)

df["text"] = (
    df["jd"] + " " + df["resume"]
)

X = df["text"]
y = df["label"]

model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            max_features=3000
        )
    ),

    (
        "clf",
        LogisticRegression()
    )

])

model.fit(
    X,
    y
)

joblib.dump(
    model,
    "models/hr_model.pkl"
)

print("✅ model trained")