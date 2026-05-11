from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

import pandas as pd


def train_ml_model(X, y):

    # =========================
    # TRAIN TEST SPLIT
    # =========================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )


    # =========================
    # CREATE MODEL
    # =========================

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )


    # =========================
    # TRAIN MODEL
    # =========================

    model.fit(X_train, y_train)


    # =========================
    # MAKE PREDICTIONS
    # =========================

    predictions = model.predict(X_test)


    # =========================
    # CALCULATE ACCURACY
    # =========================

    accuracy = accuracy_score(
        y_test,
        predictions
    )


    # =========================
    # OUTPUT RESULTS
    # =========================

    print("\nMODEL TRAINING COMPLETE\n")

    print(f"Accuracy: {accuracy:.2f}")


    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )


    return model, predictions, y_test