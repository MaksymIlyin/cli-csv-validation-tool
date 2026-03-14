import argparse
import logging
import logging.config

from datetime import datetime

from src.process import process
from conf.logger_conf import get_logging_config


logger = logging.getLogger(__name__)


def set_logger(log_level):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"app_run_{timestamp}.log"
    config = get_logging_config(log_file)
    logging.config.dictConfig(config)
    if log_level:
        logger.setLevel(log_level)


def filter_maker(level):
    level = getattr(logging, level)
    def filter(record):
        return record.levelno <= level
    return filter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI scv file validator")
    parser.add_argument("input_path", type=str, help="Path to the input file.")
    parser.add_argument("output_path", type=str, help="Path to write the output file.")
    parser.add_argument('--log_level', "-ll", type=str, choices=["INFO", "WARNING", "ERROR"])
    args = parser.parse_args()
    set_logger(args.log_level)
    logger.info("Start processing")
    process(args)
    logger.info("End processing")
