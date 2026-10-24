from pathlib import Path

import pandas as pd

DATA_FILE = Path(
    "data/raw/yellow/yellow_tripdata_2024-01.parquet"
)

COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
]


def main() -> None:
    df = pd.read_parquet(DATA_FILE, columns=COLUMNS)

    duration = (
        pd.to_datetime(df["tpep_dropoff_datetime"])
        - pd.to_datetime(df["tpep_pickup_datetime"])
    ).dt.total_seconds() / 60

    print("Extreme distance records:")
    print(
        df.nlargest(10, "trip_distance")[
            ["trip_distance", "fare_amount", "total_amount"]
        ].to_string(index=False)
    )

    print("\nMissingness overlap:")
    fields = [
        "passenger_count",
        "congestion_surcharge",
        "Airport_fee",
    ]
    print(df[fields].isna().sum())
    print(
        "All three missing:",
        int(df[fields].isna().all(axis=1).sum()),
    )

    print("\nDuration distribution (minutes):")
    print(duration.describe(percentiles=[0.5, 0.9, 0.95, 0.99]))

    print("\nNegative fare examples:")
    print(
        df.loc[
            df["fare_amount"] < 0,
            ["fare_amount", "total_amount", "trip_distance"],
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()