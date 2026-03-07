import csv
import logging
import sys

from statistics import mean

from src.data_struct import categories
from src.timed import timed
from src.validation import check_headers, check_output_folder, is_valid_row


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


def get_valid_data(file_path):
    valid_data = []
    invalid_rows_count = 0
    data = read_csv_file(file_path)
    for row_number, row in enumerate(data, 1):
        if is_valid_row(row, row_number):
            valid_data.append(row)
        else:
            invalid_rows_count += 1
    logging.info(f"Valid rows {len(valid_data)}")
    logging.info(f"Invalid rows {invalid_rows_count}")
    return valid_data


def group_data(data):
    result = []
    for category in categories:
        category_rows = list(
            filter(lambda entry: entry["category"] == category, data)
        )
        all_amount_list = [
            round(float(el["amount"]), 2) for el in category_rows
        ]
        total_amount = sum(all_amount_list)
        average_amount = round(mean(all_amount_list), 2)
        category_row = {
            "category": category,
            "row_count": len(category_rows),
            "total_amount": f"{total_amount:.2f}",
            "average_amount": f"{average_amount:.2f}",
        }
        result.append(category_row)
    return result


@timed
def process(args):
    input_path = args.input_path
    output_path = args.output_path
    check_output_folder(output_path)
    valid_data = get_valid_data(input_path)
    grouped_data = group_data(valid_data)
    write_result(output_path, grouped_data)
