from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def validate_system(
    y_true,
    y_pred
):

    return {

        "accuracy": round(
            accuracy_score(
                y_true,
                y_pred
            ) * 100,
            2
        ),

        "precision": round(
            precision_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0
            ) * 100,
            2
        ),

        "recall": round(
            recall_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0
            ) * 100,
            2
        ),

        "f1": round(
            f1_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0
            ) * 100,
            2
        )
    }