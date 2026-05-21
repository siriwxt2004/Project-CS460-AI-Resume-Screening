import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import joblib

df = pd.read_csv(
    "data/feedback.csv"
)

df["text"] = (
    df["jd"].astype(str)
    + " "
    + df["resume"].astype(str)
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
        LogisticRegression(
            max_iter=1000
        )
    )

])

model.fit(X, y)

joblib.dump(
    model,
    "models/hr_model.pkl"
)

print("✅ model trained")