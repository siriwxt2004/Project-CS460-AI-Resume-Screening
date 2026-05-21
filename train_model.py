import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import joblib
import os

# load dataset
df = pd.read_csv(
    "data/feedback.csv"
)

# combine text
df["text"] = (
    df["jd"].fillna("") + " " +
    df["resume"].fillna("")
)

X = df["text"]
y = df["label"]

# build model
model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            max_features=3000,
            stop_words="english"
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
model.fit(
    X,
    y
)

# create models folder
os.makedirs(
    "models",
    exist_ok=True
)

# save model
joblib.dump(
    model,
    "models/hr_model.pkl"
)

print("✅ model trained")