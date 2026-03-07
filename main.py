import argparse
import logging
from src.process import process


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI scv file validator")
    parser.add_argument("input_path", type=str, help="Path to the input file.")
    parser.add_argument("output_path", type=str, help="Path to write the output file.")
    parser.add_argument('--log_level', "-ll", type=str, choices=["INFO", "WARNING", "ERROR"])
    args = parser.parse_args()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=args.log_level
    )
    process(args)
