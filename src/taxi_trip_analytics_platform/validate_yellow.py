from pathlib import Path

import pandas as pd

DATA_FILE = Path(
    "data/raw/yellow/yellow_tripdata_2024-01.parquet"
)

COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "trip_distance",
    "fare_amount",
    "total_amount",
    "PULocationID",
    "DOLocationID",
]


def main() -> None:
    df = pd.read_parquet(
        DATA_FILE,
        columns=COLUMNS,
    )

    pickup = pd.to_datetime(
        df["tpep_pickup_datetime"], errors="coerce"
    )
    dropoff = pd.to_datetime(
        df["tpep_dropoff_datetime"], errors="coerce"
    )

    duration_minutes = (
        dropoff - pickup
    ).dt.total_seconds() / 60

    checks = {
        "Missing pickup timestamp": pickup.isna().sum(),
        "Missing drop-off timestamp": dropoff.isna().sum(),
        "Drop-off before pickup": (
            dropoff < pickup
        ).sum(),
        "Zero or negative distance": (
            df["trip_distance"] <= 0
        ).sum(),
        "Negative fare": (
            df["fare_amount"] < 0
        ).sum(),
        "Negative total amount": (
            df["total_amount"] < 0
        ).sum(),
        "Zero or negative duration": (
            duration_minutes <= 0
        ).sum(),
        "Duration over 24 hours": (
            duration_minutes > 24 * 60
        ).sum(),
        "Missing pickup zone": (
            df["PULocationID"].isna()
        ).sum(),
        "Missing drop-off zone": (
            df["DOLocationID"].isna()
        ).sum(),
    }

    print(f"Records checked: {len(df):,}")
    print("\nQuality checks:")
    for name, count in checks.items():
        print(f"{name}: {count:,}")

    print("\nNumeric summary:")
    print(
        df[
            ["trip_distance", "fare_amount", "total_amount"]
        ].describe().round(2)
    )


if __name__ == "__main__":
    main()