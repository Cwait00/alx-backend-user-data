#!/usr/bin/env python3
"""
Main file
"""

# Part 1: Testing filter_datum function
filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = [
    ("name=egg;email=eggmin@eggsample.com;password=eggcellent;"
     "date_of_birth=12/12/1986;"),
    ("name=bob;email=bob@dylan.com;password=bobbycool;"
     "date_of_birth=03/04/1993;")
]

print("Testing filter_datum function:")
for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

print("\nTesting RedactingFormatter class:")

# Part 2: Testing RedactingFormatter class
import logging

RedactingFormatter = __import__('filtered_logger').RedactingFormatter

message = ("name=Bob;email=bob@dylan.com;ssn=000-123-0000;"
           "password=bobby2019;")
log_record = logging.LogRecord(
    "my_logger", logging.INFO, None, None, message, None, None
)
formatter = RedactingFormatter(fields=["email", "ssn", "password"])
print(formatter.format(log_record))

print("\nTesting get_logger function and PII_FIELDS constant:")

# Part 3: Testing get_logger function and PII_FIELDS constant
get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

logger = get_logger()
logger.info(
    "This is a test log message with PII fields: name=Alice;"
    "email=alice@example.com;phone=123-456-7890;ssn=123-45-6789;"
    "password=mysecurepassword;"
)

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))
