import logging


class SqlReader:
    """SQL File Reader Class."""

    def __init__(self, logger: logging.Logger):
        """Initializes the SqlReader class."""
        self.logger = logger
        self.logger.info("SQL file reader initialized.")

    def read_sql(self, start_date: str = "", end_date: str = "") -> str:
        """Reads SQL queries from a file."""
        try:
            if self.file_path.endswith(".sql"):
                with open(self.file_path, "r") as file:
                    file_content = file.read()

                    file_content = (
                        file_content.replace("{start_date}", start_date)
                        if file_content.find("{start_date}") != -1 and start_date != ""
                        else file_content
                    )

                    file_content = (
                        file_content.replace("{end_date}", end_date)
                        if file_content.find("{end_date}") != -1 and end_date != ""
                        else file_content
                    )
                    return file_content
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
