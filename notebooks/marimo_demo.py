import marimo

app = marimo.App()


@app.cell
def __():
    import pandas as pd
    return pd


@app.cell
def __(pd):
    df = pd.DataFrame(
        {
            "client_id": [1, 2, 3],
            "balance": [1000, 2500, 1800],
            "deposit_target": [0, 1, 0],
        }
    )
    return df


@app.cell
def __(df):
    query = "SELECT client_id, balance, deposit_target FROM clients"
    print("Пример SQL-запроса:")
    print(query)
    print("\nПример DataFrame:")
    print(df)
    return query


if __name__ == "__main__":
    app.run()