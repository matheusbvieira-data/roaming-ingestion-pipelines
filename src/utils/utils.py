"""This module contains functions that can used by other modules."""

import logging
import os
import pathlib
import re
from datetime import datetime
from typing import List

import duckdb
import pandas


def is_valid_table_name(name: str) -> bool:
    """Checks if a given table name is valid.

    Returns:
        bool: True if valid or False
    """
    # Define o padrão: Começa com letra, seguido por letras, números ou underscores
    # Comprimento entre 1 e 128 caracteres
    pattern = r"^[a-zA-Z][a-zA-Z0-9_]{0,127}$"
    return bool(re.match(pattern, name))


def add_audit_columns(
    direction: str,
    source_system: str,
    job_name: str,
    job_name_abbr: str,
    teradata_user: str,
    dataframe: pandas.DataFrame,
    file: str,
    logger: logging.Logger,
) -> pandas.DataFrame:
    """Add audit columns to a given dataframe.

    Args:
        direction (str): traffic direction("INB" or "OUT")
        source_system (str): system that generated the information
        job_name (str): name of the job uploading the data
        job_name_abbr (str): abbreviation of the job name
        teradata_user (str): user that is uploading data
        dataframe (pandas.DataFrame): dataframe to be populated
        file (str): file name containing the original data
        logger (logging.Logger): logger to log information from the function

    Returns:
        pandas.DataFrame: A dataframe containing the following columns:
            DIRECTION,
            SOURCE_FILE_NAME, SOURCE_SYSTEM,
            JOB_NAME, ETL_BATCH_ID,
            ROW_CREATE_TS, ROW_CREATE_USER
    """
    logger.info("Adicionando colunas de auditoria ao arquivo")
    dataframe["DIRECTION"] = (
        direction if direction == "INB" or direction == "OUT" else ""
    )
    dataframe["SOURCE_FILE_NAME"] = file[file.rfind("\\") + 1 :]
    dataframe["SOURCE_SYSTEM"] = source_system
    dataframe["JOB_NAME"] = job_name
    dataframe["ETL_BATCH_ID"] = f"{datetime.today():%d_%m_%Y}_{job_name_abbr}"
    dataframe["ROW_CREATE_TS"] = datetime.today()
    dataframe["ROW_CREATE_USER"] = teradata_user.capitalize()
    return dataframe


def list_dates_in_file(file: str, logger: logging.Logger) -> List:
    """Retrieves all processing dates in a given file.

    Returns an empty list in case of failure.

    Args:
        file (str): file path
        logger (logging.Logger): logger to log info

    Returns:
        List: A list containing all processing dates in the given file.
    """
    query = """
        SELECT
            "TAP File (Current) Processing Date" AS TAP_FILE_CURRENT_PROCESSING_DATE,
            COUNT("Date (Call)") AS ROW_COUNT_CALL
        FROM read_csv_auto(
                ?,
                delim=';',
                encoding = 'utf-16',
                quote='"')
        WHERE 1=1
        GROUP BY TAP_FILE_CURRENT_PROCESSING_DATE;
    """
    try:
        df = duckdb.execute(query, [file]).df()
        logger.info(
            "Dates in file: %s",
            str(df["TAP_FILE_CURRENT_PROCESSING_DATE"].dt.date.unique().tolist()),
        )
    except duckdb.BinderException as e:
        logger.error("Coluna não encontrada: %s", e)
        return []
    return df["TAP_FILE_CURRENT_PROCESSING_DATE"].dt.date.unique().tolist()


def move_file(file: str, folder: pathlib.Path, logger: logging.Logger) -> bool:
    """Move a file to another folder.

    Args:
        file (str): file path
        folder (pathlib.Path): folder path
        logger (logging.Logger): logger to log info

    Returns:
        bool: True if file moved successfully otherwise False
    """
    try:
        os.rename(file, str(folder) + file[file.rfind("\\") + 1 :])
        logger.info("File %s was moved successfully!", file[file.rfind("\\") + 1 :])
        return True
    except Exception as e:
        logger.error("The following error occurred: %s", e)
        return False
