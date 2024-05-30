#!/usr/bin/env python3
"""
Module for filtering PII in log messages.
"""

import re
from typing import List


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
        separator: A string representing by which character is separating
        all fields in the log line (message).

    Returns:
        The obfuscated log message as a string.
    """
    for field in fields:
        message = re.sub(
            rf'{field}=[^{separator}]*', f'{field}={redaction}', message
        )
    return message
