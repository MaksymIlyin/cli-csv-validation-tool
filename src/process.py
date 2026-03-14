import logging

from src.data_manipulation import get_valid_data, group_data
from src.io_process import read_csv_file, write_result
from src.timed import timed
from src.validation import check_input_file, check_output_folder


logger = logging.getLogger(__name__)


@timed
def process(args):
    input_path = args.input_path
    output_path = args.output_path
    check_input_file(input_path)
    raw_data = read_csv_file(input_path)
    valid_data = get_valid_data(raw_data)
    grouped_data = group_data(valid_data)
    check_output_folder(output_path)
    write_result(output_path, grouped_data)
