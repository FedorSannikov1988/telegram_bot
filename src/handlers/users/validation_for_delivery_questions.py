"""
Validation of input parameters
(date of receipt, time of receipt,
recipient's name) for delivery.
"""
from datetime import datetime
import re


class ValidationDeliveryQuestions:
    def validation_data(self, date_string: str, format_date: str) -> bool:
        """
        Data Validation

        :param date_string: str
        :param format_date: str
        :return: bool
        """
        try:
            datetime.strptime(date_string, format_date)
            return True
        except ValueError:
            return False

    def validation_time(self, time_string: str, format_date: str) -> bool:
        """
        Time Validation

        :param time_string: str
        :param format_date: str
        :return: bool
        """
        try:
            datetime.strptime(time_string, format_date)
            return True
        except ValueError:
            return False

    def validation_name(self, text: str, max_len: int) -> bool:
        """
        Name Validation

        :param max_len: int
        :return: bool
        """
        pattern = '^[A-Za-zА-Яа-я]+$'
        return len(text) < max_len and \
            text[0].isupper() and \
            re.match(pattern, text) is not None
