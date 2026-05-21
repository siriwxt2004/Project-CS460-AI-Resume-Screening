import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# โหลด dataset
df = pd.read_csv(
    "data/feedback.csv"
)

# รวมข้อความ
df["text"] = (
    df["jd"] + " " + df["resume"]
)

X = df["text"]

y = df["label"]

# model
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

# save
joblib.dump(
    model,
    "models/hr_model.pkl"
)

print("✅ model created")