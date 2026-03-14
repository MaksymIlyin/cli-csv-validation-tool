import logging
import os
import sys

from datetime import datetime

from src.data_struct import categories, input_schema


logger = logging.getLogger(__name__)


def check_input_file(input_path):
    if not os.path.isfile(input_path):
        logger.error(f"Fatal error: input file does not exist.")
        sys.exit(0)


def check_headers(headers):
    if len(headers) != len(input_schema):
        logger.error(f"Fatal error: input file has malformed rows with inconsistent column count.")
        sys.exit(0)
    for element in input_schema:
        if element not in set(headers):
            logger.error(f"Fatal error: required header columns are missing.")
            sys.exit(0)


def check_output_folder(file_path):
    folder_path = os.path.dirname(file_path)
    if not os.path.isdir(folder_path):
        logger.warning(f"{folder_path} folder doesn't exist.")
        os.makedirs(folder_path)
        logger.info(f"{folder_path} created")


def is_valid_id(row_id, row_number):
    if not row_id.isdigit():
        logging.warning(f"Row {row_number}: {row_id=} is not an integer.")
        return False
    return True


def is_valid_category(category, row_number):
    if not category in set(categories):
        logging.warning(f"Row {row_number}: Invalid category {category=}")
        return False
    return True


def is_valid_amount(amount, row_number):
    try:
        float(amount)
    except ValueError:
        logging.warning(f"Row {row_number}: {amount=} not a float number.")
        return False
    if len(amount.split(".")[-1]) != 2:
        logging.warning(f"Row {row_number}: {amount=} don't have two numbers after point.")
        return False
    return True


def is_valid_created_at(created_at, row_number):
    try:
        created_at_datetime = datetime.strptime(created_at, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        logger.warning(f"Row {row_number}: Wrong datetime format {created_at=}")
        return False
    if datetime.now() < created_at_datetime:
        logger.warning(f"Row {row_number}: {created_at=} cannot be future datetime")
        return False
    return True


def is_valid_status(status, row_number):
    if "status" not in {"active", "inactive"}:
        logger.warning(f"Row {row_number}: Unknown status {status=}")
        return False
    return True


def is_valid_row(row, row_number):
    if None in row.values():
        logger.warning(f"Row {row_number}: There are missing columns in the {row=}")
        return False
    if '' in row.values():
        logger.warning(f"Row {row_number}: There are empty columns in the {row=}")
        return False
    if not is_valid_id(row["id"], row_number):
        return False
    if not is_valid_category(row["category"], row_number):
        return False
    if not is_valid_amount(row["amount"], row_number):
        return False
    if not is_valid_created_at(row["created_at"], row_number):
        return False
    return True
