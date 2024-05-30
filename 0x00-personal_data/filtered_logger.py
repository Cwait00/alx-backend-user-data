#!/usr/bin/env python3
"""
Module for filtering PII in log messages and connecting to a secure database.
"""

import os
import re
import logging
import mysql.connector
from typing import List, Tuple


# Define PII_FIELDS constant
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Returns the log message obfuscated.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all
                   fields in the log line (message).

    Returns:
        The obfuscated log message as a string.
    """
    for field in fields:
        message = re.sub(
            rf'{field}=[^{separator}]*', f'{field}={redaction}', message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize the formatter with fields to redact """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record, redacting sensitive information """
        original_message = super(RedactingFormatter, self).format(record)
        redacted_message = filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )
        return redacted_message


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named 'user_data' with a stream handler
    using RedactingFormatter.

    Returns:
        A logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database.

    Uses credentials from environment variables:
    - PERSONAL_DATA_DB_USERNAME
    - PERSONAL_DATA_DB_PASSWORD
    - PERSONAL_DATA_DB_HOST
    - PERSONAL_DATA_DB_NAME

    Returns:
        A MySQLConnection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main():
    """
    Retrieves all rows in the users table and logs each row in a filtered
    format.
    """
    logger = get_logger()

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()

        for row in rows:
            filtered_data = {
                key: filter_datum(PII_FIELDS, "***", str(value), ";")
                for key, value in row.items()
            }
            log_message = "; ".join(
                f"{key}={value}" for key, value in filtered_data.items()
            )
            logger.info(log_message)

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()
            logger.info("MySQL connection closed")


# Run main function if executed directly
if __name__ == "__main__":
    main()
