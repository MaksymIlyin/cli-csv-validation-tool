import logging
from statistics import mean

from src.data_struct import categories
from src.validation import is_valid_row


logger = logging.getLogger(__name__)


def get_valid_data(raw_data):
    valid_data = []
    invalid_rows_count = 0
    for row_number, row in enumerate(raw_data, 1):
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
        if all_amount_list:
            total_amount = sum(all_amount_list)
            average_amount = round(mean(all_amount_list), 2)
        else:
            total_amount = 0.00
            average_amount = 0.00
        category_row = {
            "category": category,
            "row_count": len(category_rows),
            "total_amount": f"{total_amount:.2f}",
            "average_amount": f"{average_amount:.2f}",
        }
        result.append(category_row)
    return result
