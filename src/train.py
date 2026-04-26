from pathlib import Path
import json
import pickle

import mlflow
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


TRAIN_PATH = "data/processed/train.csv"
TEST_PATH = "data/processed/test.csv"
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "model.pkl"
METRICS_PATH = Path("metrics.json")
TARGET_COLUMN = "target"


def main() -> None:
    with open("params.yaml", "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)

    model_name = params["train"]["model_name"]
    max_iter = params["train"]["max_iter"]
    random_state = params["train"]["random_state"]

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    model = LogisticRegression(
        max_iter=max_iter,
        random_state=random_state
    )

    mlflow.set_experiment("hw5_mlops_experiment")

    with mlflow.start_run():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        MODEL_DIR.mkdir(parents=True, exist_ok=True)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        metrics = {"accuracy": float(acc)}
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)

        mlflow.log_param("model_name", model_name)
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("random_state", random_state)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_artifact(str(MODEL_PATH))
        mlflow.log_artifact(str(METRICS_PATH))

    print("Обучение модели завершено")
    print(f"Accuracy: {acc}")


if __name__ == "__main__":
    main()