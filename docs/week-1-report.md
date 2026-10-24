# Week 1 Report — NYC TLC Yellow Taxi Analytics Capstone

**Project:** NYC TLC Taxi Trip Analytics Platform  
**Milestone:** Week 1 — Project Setup and Data Exploration  
**Dataset:** NYC Yellow Taxi Trip Records, January 2024  
**Status:** Completed

## 1. Executive Summary

During Week 1, the project environment was established and the January 2024 NYC Taxi and Limousine Commission (TLC) Yellow Taxi dataset was downloaded and analyzed.

The dataset contains **2,964,624 records and 19 columns**, stored in Parquet format. Initial analysis covered schema inspection, missing-value profiling, numeric distributions, timestamp consistency, trip distances, fare amounts, and trip durations.

The investigation identified missing values in five columns, negative fare and total amounts, zero or negative trip distances, invalid timestamp ordering, and extreme trip-distance and duration values.

A key finding is that **140,162 records (4.73%) have missing values in five columns**. All records with a missing `passenger_count` have `payment_type = 0`, which the supplied TLC data dictionary identifies as a Flex Fare trip. The reason for this relationship has not yet been established.

No destructive data cleaning was performed. The source dataset remains unchanged, and the findings will inform explicit, testable transformation rules in later milestones.

## 2. Objectives

The objectives for Week 1 were to:

1. Establish a Python development environment using `uv`.
2. Initialize the project structure and prepare it for version control.
3. Download an official TLC Yellow Taxi dataset.
4. Inspect the Parquet schema and record structure.
5. Profile missing values and numeric distributions.
6. Validate basic temporal and numerical data-quality conditions.
7. Investigate anomalous records and missingness patterns.
8. Document findings and define the next implementation steps.

## 3. Project Scope

### In scope

- Yellow Taxi trip records only.
- January 2024 as the initial analysis period.
- Local development and exploratory analysis.
- Parquet schema inspection and data profiling.
- Preliminary data-quality checks.
- Documentation of findings and follow-up work.

### Out of scope for Week 1

- Green Taxi datasets.
- Automated scheduled ingestion.
- Spark-based distributed transformations.
- Airflow orchestration.
- MinIO deployment.
- Analytical SQL models and dashboards.
- Production deployment and performance optimization.

These capabilities are planned for subsequent milestones.

## 4. Development Environment and Tools

The project uses Python 3.13 and `uv` for Python environment and dependency management.

| Component | Purpose |
|---|---|
| Python 3.13 | Project programming language |
| `uv` | Dependency and environment management |
| pandas | Exploratory data analysis |
| PyArrow | Parquet reading, schema inspection, and profiling |
| pytest | Automated testing |
| Ruff | Linting and code quality |
| Git | Source control and milestone tracking |
| Parquet | Source dataset format |

Compatibility with additional frameworks will be verified when those dependencies are introduced.

## 5. Dataset Description

### 5.1 Data source

**Publisher:** New York City Taxi and Limousine Commission (TLC)

Official data page:  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

January 2024 Yellow Taxi Parquet file:

https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet

Expected local path:

`data/raw/yellow/yellow_tripdata_2024-01.parquet`

### 5.2 Dataset overview

| Property | Result |
|---|---|
| Taxi type | Yellow Taxi |
| Reporting period | January 2024 |
| Format | Apache Parquet |
| Number of records | 2,964,624 |
| Number of columns | 19 |
| Parquet row groups | 3 |
| Columns containing missing values | 5 |
| Original data modified | No |

### 5.3 Schema

| Column | Description |
|---|---|
| `VendorID` | Taxi technology provider identifier |
| `tpep_pickup_datetime` | Meter-engaged timestamp |
| `tpep_dropoff_datetime` | Meter-disengaged timestamp |
| `passenger_count` | Reported passenger count |
| `trip_distance` | Meter-reported trip distance in miles |
| `RatecodeID` | Final trip rate code |
| `store_and_fwd_flag` | Store-and-forward indicator |
| `PULocationID` | TLC pickup taxi-zone identifier |
| `DOLocationID` | TLC drop-off taxi-zone identifier |
| `payment_type` | Payment or trip category code |
| `fare_amount` | Meter-based fare |
| `extra` | Miscellaneous extras and surcharges |
| `mta_tax` | MTA tax |
| `tip_amount` | Recorded tip amount; cash tips are excluded |
| `tolls_amount` | Recorded toll charges |
| `improvement_surcharge` | Improvement surcharge |
| `total_amount` | Total passenger charge, excluding cash tips |
| `congestion_surcharge` | Congestion surcharge |
| `Airport_fee` | Airport fee associated with qualifying airport pickups |

The January 2024 schema does not contain `cbd_congestion_fee`. The pipeline will need to account for schema evolution when data from periods containing this field is introduced.

## 6. Data Profiling Results

### 6.1 Missing values

Five columns contain missing values. Each has exactly 140,162 nulls, representing approximately 4.73% of all records.

| Column | Missing records | Missing percentage |
|---|---:|---:|
| `passenger_count` | 140,162 | 4.73% |
| `RatecodeID` | 140,162 | 4.73% |
| `store_and_fwd_flag` | 140,162 | 4.73% |
| `congestion_surcharge` | 140,162 | 4.73% |
| `Airport_fee` | 140,162 | 4.73% |
| All other columns | 0 | 0.00% |

The identical null counts and investigation results show that these five columns are missing together for the same records.

This pattern does not establish a definitive cause. It may be related to a trip category or source-system behavior, but further investigation is needed.

### 6.2 Numeric summary

| Metric | Mean | Median | Minimum | Maximum |
|---|---:|---:|---:|---:|
| `trip_distance` (miles) | 3.65 | 1.68 | 0 | 312,722.30 |
| `fare_amount` | 18.18 | — | -899 | 5,000 |
| `total_amount` | 26.80 | — | -900 | 5,000 |

The standard deviation of `trip_distance` is approximately 225.46 miles. This is unusually high for ordinary urban taxi trips and is heavily influenced by extreme values.

The maximum distance of 312,722.30 miles is implausible for a normal NYC taxi journey. Median and percentile statistics are therefore more representative than the mean for many descriptive analyses.

### 6.3 Trip duration

Trip duration was calculated as the difference between the drop-off and pickup timestamps.

| Statistic | Duration |
|---|---:|
| Mean | 15.61 minutes |
| Median | 11.63 minutes |
| 90th percentile | 28.87 minutes |
| 95th percentile | 37.93 minutes |
| 99th percentile | 60.45 minutes |
| Minimum | -13.57 minutes |
| Maximum | 9,455.40 minutes |

The maximum duration is approximately 6.57 days, which is implausible for an ordinary taxi trip.

Negative durations indicate that drop-off timestamps precede pickup timestamps. Very long durations may reflect erroneous records, unusual operational cases, or other source-data issues. These records should be investigated before exclusion rules are defined.

## 7. Data Quality Assessment

The initial validation checks produced the following results:

| Check | Records flagged |
|---|---:|
| Missing pickup timestamp | 0 |
| Missing drop-off timestamp | 0 |
| Drop-off earlier than pickup | 56 |
| Zero or negative trip distance | 60,371 |
| Negative fare amount | 37,448 |
| Negative total amount | 35,504 |
| Zero or negative trip duration | 870 |
| Trip duration over 24 hours | 16 |
| Missing pickup zone | 0 |
| Missing drop-off zone | 0 |

These counts represent individual checks and may overlap. They must not be summed to calculate a total number of invalid records.

### 7.1 Trip-distance anomalies

There are 60,371 records with zero or negative trip distances. Extremely large positive distances are also present.

These values can distort trip-distance summaries, fare-per-mile calculations, and distance-based visualizations.

**Planned treatment:** preserve the source records and flag invalid or implausible distances in the cleaned layer. Define inclusion rules according to the requirements of each analytical metric.

### 7.2 Negative fares and total amounts

The dataset contains 37,448 negative `fare_amount` values and 35,504 negative `total_amount` values.

Negative values may represent refunds, adjustments, reversals, or other special cases. The current investigation does not establish the reason for each record.

**Planned treatment:** investigate affected records before excluding them. Negative amounts will not automatically be deleted or converted to zero.

### 7.3 Timestamp inconsistencies

Fifty-six records have drop-off timestamps earlier than pickup timestamps. A total of 870 records have zero or negative calculated duration, and 16 records have durations exceeding 24 hours.

The categories can overlap. In particular, records with drop-off timestamps before pickup are also expected to have negative durations.

**Planned treatment:** implement explicit timestamp-consistency flags during transformation. Invalid timestamp ordering will be treated separately from unusually long durations.

### 7.4 Location identifiers

No pickup or drop-off location identifiers are missing.

However, `PULocationID` and `DOLocationID` are TLC taxi-zone identifiers rather than latitude and longitude coordinates. Geographic analysis will require a suitable TLC taxi-zone lookup dataset.

### 7.5 Financial metric interpretation

`total_amount` represents the recorded total passenger charge and is not equivalent to taxi-company revenue or net profit.

`tip_amount` excludes cash tips, so recorded tip values do not represent every tip paid to a driver.

These distinctions must be reflected in the definitions of future analytical metrics.

## 8. Missingness Investigation: Flex Fare

The supplied TLC data dictionary defines `payment_type = 0` as a **Flex Fare trip**. This is a valid category, not an unknown or invalid payment type.

The investigation found:

- 140,162 records have missing `passenger_count`.
- All records in this group have `payment_type = 0`.
- The group includes 91,447 records with `VendorID = 2`, 48,455 with `VendorID = 1`, and 260 with `VendorID = 6`.
- The same records have null values in `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`.

The median values for selected metrics differ between the two groups:

| Metric | Missing `passenger_count` | Non-missing `passenger_count` |
|---|---:|---:|
| `trip_distance` | 1.95 miles | 1.67 miles |
| `fare_amount` | 16.82 | 12.80 |
| `total_amount` | 21.86 | 20.00 |

These are descriptive differences and do not establish causation.

The analysis establishes that missing passenger counts are associated with the Flex Fare category in this dataset. It does not establish why the fields are missing or whether all Flex Fare records have missing passenger counts. The latter should be verified explicitly.

**Decision:** retain these records and preserve their null values. Do not infer passenger counts or replace missing charges with zero without supporting evidence.

Suggested documentation statement:

> In the January 2024 Yellow Taxi dataset, 140,162 records (4.73%) have missing passenger counts, and all of these records have `payment_type = 0`, corresponding to Flex Fare trips. These records are retained pending further analysis; missing fields are not automatically replaced with zero.

## 9. Data Handling Principles

The following principles will guide subsequent development:

1. **Preserve raw data.** Original Parquet files remain immutable pipeline inputs.
2. **Make cleaning explicit.** Transformation rules must be documented and testable.
3. **Distinguish missing from zero.** Null values must not automatically be replaced with zero.
4. **Preserve valid categories.** Flex Fare (`payment_type = 0`) is valid according to the supplied data dictionary.
5. **Flag before excluding.** Investigate anomalies before deciding whether to exclude them from a specific metric.
6. **Avoid unsupported assumptions.** Unusual negative amounts and missingness patterns require further investigation.
7. **Account for schema evolution.** Future datasets may contain columns absent from the January 2024 schema.
8. **Make processing reproducible.** Scripts should run from the project root using the managed environment.

## 10. Project Artifacts and Reproducibility

The Week 1 exploratory scripts include:

- `inspect_yellow.py` — inspect the dataset schema and structure.
- `profile_yellow.py` — profile null counts and column statistics.
- `validate_yellow.py` — execute basic data-quality checks.
- `investigate_yellow.py` — investigate extreme values and duration distributions.
- `investigate_missingness.py` — examine the relationship between missing values and trip categories.

The Python package is `taxi_trip_analytics_platform`.

Run the scripts from the repository root.

### Windows PowerShell

```powershell
uv run python -m taxi_trip_analytics_platform.inspect_yellow
uv run python -m taxi_trip_analytics_platform.profile_yellow
uv run python -m taxi_trip_analytics_platform.validate_yellow
uv run python -m taxi_trip_analytics_platform.investigate_yellow
uv run python -m taxi_trip_analytics_platform.investigate_missingness
```

### Linux Bash

```bash
uv run python -m taxi_trip_analytics_platform.inspect_yellow
uv run python -m taxi_trip_analytics_platform.profile_yellow
uv run python -m taxi_trip_analytics_platform.validate_yellow
uv run python -m taxi_trip_analytics_platform.investigate_yellow
uv run python -m taxi_trip_analytics_platform.investigate_missingness
```

The exploratory scripts should be committed to version control. The raw Parquet dataset should generally remain outside Git unless the repository intentionally uses Git LFS or another data-versioning mechanism.

## 11. Limitations

This report is based on one month of Yellow Taxi data. The findings should not automatically be generalized to other months, taxi types, or years.

The analysis has not established the causes of missing values or negative financial amounts. It has also not verified every anomaly against external records.

The current validation checks are preliminary and do not constitute a complete production data-quality framework.

Finally, a flagged record is not necessarily invalid for every analytical purpose. Final inclusion criteria will depend on the analytical question and documented business rules.

## 12. Week 1 Completion Assessment

| Deliverable | Status |
|---|---|
| Python project environment established | Completed |
| Yellow Taxi source data downloaded | Completed |
| Parquet schema inspected | Completed |
| Missing values profiled | Completed |
| Basic data-quality checks run | Completed |
| Extreme values investigated | Completed |
| Missingness pattern investigated | Completed |
| Initial findings documented | Completed |
| Automated repeatable ingestion | Planned |
| Formal transformation and cleaning rules | Planned |
| Analytical models and dashboards | Planned |

Week 1 is considered complete because the environment, source dataset, initial profiling, and preliminary quality assessment have been established.

## 13. Week 2 Plan: Repeatable Ingestion and Raw Storage

Week 2 will focus on making dataset acquisition and raw-data storage repeatable.

Planned tasks:

1. Create a reusable ingestion module instead of relying on manual downloads.
2. Record source URLs, dataset period, ingestion timestamp, and local file path.
3. Make ingestion idempotent so rerunning it does not create unnecessary duplicate files.
4. Validate that downloaded files exist, are non-empty, and can be read as Parquet.
5. Keep raw files unchanged and separate from cleaned outputs.
6. Add tests for ingestion behavior and failure cases.
7. Document ingestion instructions in the README.
8. Decide when to introduce MinIO without making it a prerequisite for local ingestion.

**Expected outcome:** a repeatable and testable way to retrieve and store Yellow Taxi source data while preserving the original files and their provenance.

## 14. Conclusion

Week 1 established the foundation for the NYC TLC Yellow Taxi Analytics Capstone. The January 2024 dataset was downloaded, its schema and distributions were inspected, and the principal data-quality issues were recorded.

The most important findings are the shared missingness pattern affecting 140,162 records, implausible trip distances, negative financial values, and inconsistent or extreme trip durations. The investigation also clarified that `payment_type = 0` represents Flex Fare and is a valid category.

These findings will inform future ingestion validation and cleaning logic. Preserving raw data and postponing irreversible decisions until rules are justified will help make the analytics pipeline transparent, reproducible, and trustworthy.
