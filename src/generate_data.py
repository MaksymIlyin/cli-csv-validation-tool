import argparse
import csv
import random

from datetime import datetime, timedelta

from timed import timed
from data_struct import categories, input_schema


@timed
def generate_scv(rows_number, file_path):
    with open(file_path, "w", newline="") as csv_file:
        fieldnames = list(input_schema)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row_number in range(rows_number):
            now = datetime.now()
            creation_time = now - timedelta(seconds=random.randint(2_000, 20_000))
            row = {
                "id": row_number,
                "category": random.choice(categories),
                "amount": f"{round(random.uniform(0.0, 50.0), 2):.2f}",
                "created_at": creation_time.strftime("%Y-%m-%d-%H:%M:%S"),
                "status": random.choice(["active", "inactive"])
            }
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", "-r", type=int, help="Number of rows to generate in file")
    parser.add_argument("--path", "-p", type=str, help="Path to write the file")
    args = parser.parse_args()
    generate_scv(args.rows, args.path)
