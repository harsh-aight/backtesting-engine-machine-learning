# ml/train_model.py

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


def train_ml_model(X, y):

    # =========================
    # TIME SERIES SPLIT
    # =========================

    split_index = int(len(X) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # =========================
    # MODEL
    # =========================

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    # =========================
    # TEST PREDICTIONS
    # =========================

    predictions = model.predict(X_test)

    # =========================
    # METRICS
    # =========================

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nMODEL TRAINING COMPLETE\n")

    print(f"Accuracy: {accuracy:.2f}")

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    return model, X_test, y_test