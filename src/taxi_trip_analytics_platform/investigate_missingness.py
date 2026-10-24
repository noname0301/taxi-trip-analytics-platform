from pathlib import Path

import pandas as pd

DATA_FILE = Path(
    "data/raw/yellow/yellow_tripdata_2024-01.parquet"
)


def main() -> None:
    columns = [
        "VendorID",
        "passenger_count",
        "RatecodeID",
        "store_and_fwd_flag",
        "payment_type",
        "congestion_surcharge",
        "Airport_fee",
        "trip_distance",
        "fare_amount",
        "total_amount",
    ]

    df = pd.read_parquet(DATA_FILE, columns=columns)

    missing = df["passenger_count"].isna()

    print("Records with passenger_count missing:")
    print(f"{missing.sum():,} ({missing.mean():.2%})")

    print("\nVendorID distribution: missing group")
    print(df.loc[missing, "VendorID"].value_counts(dropna=False))

    print("\nVendorID distribution: non-missing group")
    print(df.loc[~missing, "VendorID"].value_counts(dropna=False))

    print("\nPayment type: missing group")
    print(df.loc[missing, "payment_type"].value_counts(dropna=False))

    print("\nDistance summary by missingness group:")
    print(
        df.assign(passenger_count_missing=missing)
        .groupby("passenger_count_missing")[
            ["trip_distance", "fare_amount", "total_amount"]
        ]
        .median()
        .round(2)
    )


if __name__ == "__main__":
    main()