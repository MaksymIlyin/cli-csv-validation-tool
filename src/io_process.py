import csv
import logging
import sys

from src.validation import check_headers


logger = logging.getLogger(__name__)


def read_csv_file(file_path):
    data = []
    logger.info(f"Get data from input file {file_path}")
    try:
        with open(file_path, "r", newline="") as input_file:
            reader = csv.DictReader(input_file)
            headers = reader.fieldnames
            check_headers(headers)
            for row in reader:
                data.append(row)
        logging.info(f"There are {len(data)} rows of data.")

        return data
    except Exception as e:
        logger.error(f"During working with file an error occurred {e}")
        sys.exit(0)


def write_result(file_path, grouped_data):
    fieldnames = list(grouped_data[0].keys())
    with open(file_path, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(grouped_data)
    logger.info(f"Process finished. Saved result to the {file_path}")
