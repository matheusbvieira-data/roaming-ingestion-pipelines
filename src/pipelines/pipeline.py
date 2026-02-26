"""Default pipeline module."""

import logging


class Pipeline:
    """Default pipeline class."""

    def __init__(
        self,
    ):  # logger: logging.Logger):
        """Initializes pipeline.

        Args:
            logger (logging.Logger): a logger to log class info.
        """
        # logger.info("Inicializando pipeline...")
        ...

    def extract(self): ...

    def transform(self): ...

    def load(self): ...

    def run(self):
        """Standard run method."""
        self.extract()
        self.transform()
        self.load()
