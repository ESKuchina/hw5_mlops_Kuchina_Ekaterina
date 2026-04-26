from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


RAW_PATH = "data/raw/data.csv"
OUTPUT_DIR = Path("data/processed")
TARGET_COLUMN = "target"


def main() -> None:
    with open("params.yaml", "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)

    test_size = params["prepare"]["test_size"]
    random_state = params["prepare"]["random_state"]

    df = pd.read_csv(RAW_PATH)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    train_df = X_train.copy()
    train_df[TARGET_COLUMN] = y_train

    test_df = X_test.copy()
    test_df[TARGET_COLUMN] = y_test

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
    test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)

    print("Подготовка данных завершена")
    print(f"Train shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")


if __name__ == "__main__":
    main()