import logging
import sys

def get_logger(name, level=logging.INFO, log_to_file=False, log_file="app.log"):
    """
    Creates and configures a logger.
    Args:
        name (str): Name of the logger.
        level (int): Logging level (default is logging.INFO).
        log_to_file (bool): If True, logs will also be written to a file.
        log_file (str): Path to the log file (default is 'app.log').
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:  # Avoid adding multiple handlers
        # Stream handler for console logging
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Optional file handler for logging to a file
        if log_to_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Custom flushing stream handler to ensure immediate output
        class FlushingStreamHandler(logging.StreamHandler):
            def emit(self, record):
                super().emit(record)
                self.flush()

        logger.addHandler(FlushingStreamHandler())

    # Set the logger level
    logger.setLevel(level)

    return logger