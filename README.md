This is a README for the CLI Tool.

Argparse docs - https://docs.python.org/3.14/library/argparse.html

Argparse tutorial - https://docs.python.org/3.14/howto/argparse.html#argparse-tutorial

Logging docs - https://docs.python.org/3/library/logging.html

# Transaction CSV Processor

This CLI tool reads a CSV file with transaction data, validates file structure and row values, skips invalid rows, aggregates valid rows by category, and writes the aggregated result to an output CSV file.

## Input schema

Required columns:
- id: integer
- category: one of [books, food, tools, games, music]
- amount: float, must be >= 0
- created_at: datetime in format `%Y-%m-%d %H:%M:%S`
- status: one of [active, inactive]

Column order does not matter.
Required column names must exist.

## Validation

Fatal errors:
- input file does not exist
- required header columns are missing
- file cannot be parsed structurally

Recoverable row errors:
- invalid id
- invalid category
- invalid amount
- invalid datetime format
- future datetime
- invalid status

Invalid rows are skipped and counted.

## Output schema

The tool writes an aggregated CSV with columns:
- category
- row_count
- total_amount
- average_amount

Rows are grouped by category.
Numeric values are written with 2 decimal places.
Rows are sorted by category ascending.

## Usage

Generate data

```bash
python3 ./src/generate_data.py -r 400000 -p ./input/file.csv
```

Run validator

```bash
python3 main.py ./input/file.csv ./output/result.csv --log-level INFO
```

---

## 6. Example input/output

Input example

```
created_at,status,category,amount,id
2026-03-07-14:54:12,inactive,food,4.47,0
2026-03-07-17:45:01,inactive,food,36.52,1
2026-03-07-17:57:05,inactive,tools,12.92,2
2026-03-07-17:33:43,active,games,48.62,3
2026-03-07-14:41:08,active,music,39.08,4
...
```

Output example

```
category,row_count,total_amount,average_amount
books,80085,2005135.40,25.04
food,79714,1995972.95,25.04
tools,79666,1996238.95,25.06
games,79914,1995281.02,24.97
music,80603,2017772.49,25.03
```
