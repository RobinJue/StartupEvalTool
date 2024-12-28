import logging
import sys

def configure_logger():
    """
    Configures the root logger for the entire application.
    Ensures immediate flushing and consistent formatting.
    """
    # Get the root logger
    root_logger = logging.getLogger()

    # Remove any existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    # Define a custom flushing stream handler
    class FlushingStreamHandler(logging.StreamHandler):
        def emit(self, record):
            super().emit(record)
            self.flush()

    # Create and configure the handler
    handler = FlushingStreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)