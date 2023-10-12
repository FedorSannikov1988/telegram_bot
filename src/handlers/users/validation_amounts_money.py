"""
Validation of the entered amount
"""
import re


class ValidationAmountsMoney:
    def validation_amount(self, money: str, min: int, multiplicity: int) -> bool:
        """
        Validation function of the entered amount
        :param money: str
        :param min: int
        :param multiplicity: int
        :return: bool
        """
        pattern = '[0-9]+'
        return \
                re.match(pattern, money) is not None and \
                int(money) >= min and \
                int(money) % multiplicity == 0


