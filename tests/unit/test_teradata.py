import logging
import os
import sys
from typing import Any

import pandas
import pytest
from dotenv import load_dotenv

from src.connectors.teradata import TeradataConnection, main  # type: ignore
from src.utils.logger import Logger

load_dotenv()

HOST = str(os.getenv("TERADATA_HOST"))
USER = str(os.getenv("TERADATA_USER"))
PWD = str(os.getenv("TERADATA_PASSWORD"))
DB = str(os.getenv("TERADATA_DB"))


class TestTeradataConnection:
    """Set of tests to teradata connector class."""

    @pytest.fixture
    def teradata_connection(self):
        """Returns a teradata connection object.

        Returns:
            TeradataConnection: TeradataConnection object
        """
        logger = Logger("test_job").get_logger()
        conn = TeradataConnection(logger)
        return conn

    @pytest.mark.parametrize(
        "host, expected",
        [(HOST, True), (HOST[:-4], False)],
    )
    @pytest.mark.skipif(
        sys.platform.startswith("linux"),
        reason="This will not run on actions. It needs to be connected to TBRA VPN",
    )
    def test_connection(
        self, host: str, teradata_connection: TeradataConnection, expected: bool
    ):
        """Test connection function."""
        teradata_connection.close_connection()
        assert (
            teradata_connection.create_connection(
                host=host,
                user=USER,
                pwd=PWD,
                db=DB,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "dataframe, expected",
        [
            (
                pandas.DataFrame.from_dict(
                    {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
                ),
                (4, 2),
            ),
            (
                [1, 2, 3],
                None,
            ),
        ],
    )
    def test_save_errors(
        self,
        dataframe: Any,
        expected: tuple[int, int],
        teradata_connection: TeradataConnection,
    ):
        """Test save erros function.

        Args:
            dataframe (Any): data to save
            expected (tuple[int, int]): expected return values
            teradata_connection (TeradataConnection): TeradataConnection object
        """
        assert teradata_connection._save_errors(dataframe) == expected  # type: ignore

    @pytest.mark.parametrize(
        "value, expected",
        [
            (1, logging.Logger),
            (Logger("test_job").get_logger(), logging.Logger),
        ],
    )
    def test_set_logger(
        self, value: Any, expected: Any, teradata_connection: TeradataConnection
    ):
        """Test logger setter.

        Args:
            value (Any): Any value
            expected (Any): Expected value
            teradata_connection (TeradataConnection): TeradataConnection object
        """
        teradata_connection.logger = value
        assert type(teradata_connection.logger) is expected


@pytest.mark.skipif(
    sys.platform.startswith("linux"),
    reason="This will not run on actions. It needs to be connected to TBRA VPN",
)
def test_main_no_args(capsys):  # type: ignore
    """Call the main function directly with specific arguments for testing."""
    main(args=None)
    captured = capsys.readouterr()  # type: ignore
    assert captured.out == ""  # type: ignore
