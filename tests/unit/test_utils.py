import os
import pathlib
from typing import List

import pytest

from src.utils.utils import delete_files, find_files, unzip_files

TESTED_FOLDER = (
    r"C:\Users\a0153041\OneDrive - Telefonica\09 - Bases\00 - DCH to Teradata"
)


@pytest.mark.parametrize(
    "folder_path, prefix, date_sensitive, return_first, expected",
    [
        (
            pathlib.Path(TESTED_FOLDER),
            "Daily_National_for_Teradata_Outbound",
            False,
            False,
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\Daily_National_for_Teradata_Outbound_2026-02-26.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\Daily_National_for_Teradata_Outbound_2026-02-25.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\Daily_National_for_Teradata_Outbound_2026-02-24.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\Daily_National_for_Teradata_Outbound_2026-02-23.zip"
                ),
            ],
        ),
        (
            pathlib.Path(TESTED_FOLDER),
            "Daily_International_for_TERADATA_OUT_USA",
            True,
            True,
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.zip"
                ),
            ],
        ),
        (
            pathlib.Path(TESTED_FOLDER),
            "Daily_International_for_TERADATA_OUT_USA",
            False,
            False,
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-25.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-24.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-23.zip"
                ),
            ],
        ),
        (
            pathlib.Path(TESTED_FOLDER),
            "Daily_International_for_TERADATA_OUT",
            True,
            False,
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_ARG_2026-02-26.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_OTHERS_2026-02-26.zip"
                ),
            ],
        ),
    ],
)
def test_find_files(
    folder_path: pathlib.Path,
    prefix: str,
    date_sensitive: bool,
    return_first: bool,
    expected: List[pathlib.Path],
):
    """Test find files funcion with given parameters."""
    print(find_files(folder_path, prefix, date_sensitive, return_first))
    assert find_files(folder_path, prefix, date_sensitive, return_first) == expected


@pytest.mark.parametrize(
    "paths, pwd, expected",
    [
        (
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.zip"
                ),
            ],
            "87654321",
            None,
        ),
        (
            None,
            None,
            None,
        ),
        (
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.zip"
                ),
            ],
            "roaming_pipelines_teradata",
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.csv"
                ),
            ],
        ),
        (
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.zip"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-25.zip"
                ),
            ],
            "roaming_pipelines_teradata",
            [
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-26.csv"
                ),
                pathlib.Path(
                    TESTED_FOLDER
                    + r"\\Daily_International_for_TERADATA_OUT_USA_2026-02-25.csv"
                ),
            ],
        ),
    ],
)
def test_unzip_files(
    paths: List[pathlib.Path], pwd: str | None, expected: List[pathlib.Path]
):
    """Tests unzip file function."""
    test_return = unzip_files(paths, pwd)
    try:
        for path in expected:
            os.remove(path)
    except TypeError:
        ...
    assert test_return == expected


@pytest.mark.parametrize("paths, expected", [(None, None)])
def test_delete_files(paths: List[pathlib.Path], expected: None):
    """Tests delete_files function.

    Args:
        paths (List[pathlib.Path]): A list of paths
        expected (None): This function always return None
    """
    assert delete_files(paths) == expected
