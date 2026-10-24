from pathlib import Path

import pyarrow.parquet as pq

DATA_FILE = Path(
    "data/raw/yellow/yellow_tripdata_2024-01.parquet"
)


def main() -> None:
    parquet_file = pq.ParquetFile(DATA_FILE)
    schema = parquet_file.schema_arrow
    total_rows = parquet_file.metadata.num_rows

    print(f"Total rows: {total_rows:,}")
    print(f"Total columns: {len(schema.names)}")
    print("\nColumn names:")
    for name in schema.names:
        print(f"- {name}")

    null_counts = {name: 0 for name in schema.names}
    rows_processed = 0

    for batch in parquet_file.iter_batches(
        batch_size=100_000
    ):
        rows_processed += batch.num_rows
        for i, name in enumerate(batch.schema.names):
            null_counts[name] += batch.column(i).null_count

    print("\nMissing-value report:")
    for name, count in null_counts.items():
        percentage = (
            count / total_rows * 100 if total_rows else 0
        )
        print(
            f"{name}: {count:,} missing "
            f"({percentage:.2f}%)"
        )


if __name__ == "__main__":
    main()