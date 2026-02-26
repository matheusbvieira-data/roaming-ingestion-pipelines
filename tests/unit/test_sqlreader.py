import pytest

import src.utils.logger as logger
import src.utils.sqlreader as sqlreader


class TestSqlReader:
    @pytest.fixture
    def sql_reader(self):
        test_logger = logger.Logger(
            name="test-logger", level=logger.logging.DEBUG
        ).get_logger()
        reader = sqlreader.SqlReader(logger=test_logger)
        return reader

    def test_set_file_path(self, sql_reader):
        test_path = "sql/test_query.sql"
        sql_reader.set_file_path(test_path)
        assert sql_reader.file_path == test_path

    def test_read_sql_valid_file(self, sql_reader, tmp_path):
        sql_reader.set_file_path("tests/sql/test_query.sql")
        result = sql_reader.read_sql(start_date="2024-01-01", end_date="2024-06-30")
        expected_result = "SELECT * FROM test_table WHERE date >= '2024-01-01' AND date <= '2024-06-30';"
        assert result == expected_result

    def test_read_sql_invalid_file_type(self, sql_reader, tmp_path):
        sql_reader.set_file_path("tests/sql/test_query.txt")
        result = sql_reader.read_sql()
        assert result == ""

    def test_read_sql_file_not_found(self, sql_reader):
        sql_reader.set_file_path("non_existent_file.sql")
        result = sql_reader.read_sql()
        assert result == ""

    def test_read_sql_no_file_path_set(self, sql_reader):
        result = sql_reader.read_sql()
        assert result == ""
