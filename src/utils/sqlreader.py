import logging


class SqlReader:
    """SQL File Reader Class."""

    def __init__(self, logger: logging.Logger):
        """Initializes the SqlReader class."""
        self.logger = logger
        self.logger.info("SQL file reader initialized.")

    def read_sql(self) -> str:
        """Reads SQL queries from a file."""
        try:
            if self.file_path.endswith(".sql"):
                with open(self.file_path, "r") as file:
                    return file.read()
            else:
                self.logger.error("Invalid file type: %s", self.file_path)
        except AttributeError:
            self.logger.error("File path is not set.")
        except FileNotFoundError:
            self.logger.error("SQL file not found: %s", self.file_path)
        return ""

    def set_file_path(self, file_path: str) -> None:
        """Sets the SQL file path."""
        self.file_path = file_path
        self.logger.info("SQL file path set to %s", self.file_path)
