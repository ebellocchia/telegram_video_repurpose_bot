# Copyright (c) 2026 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
import secrets
import string
from typing import List


class RandomUtils:
    """
    Provides cryptographically secure random value generation utilities.

    Generates random floats, integers, hexadecimal strings, and alphanumeric
    strings using secure methods with configurable ranges and precision.
    """

    @staticmethod
    def RandomFloat(min_val: float,
                    max_val: float,
                    precision: int = 3) -> float:
        """
        Generate a random float within a range.

        Uses random.uniform (not secrets) as this is intended for non-security
        purposes (filter value randomization).

        Args:
            min_val: The minimum value (inclusive).
            max_val: The maximum value (inclusive).
            precision: Number of decimal places. Defaults to 3.

        Returns:
            A random float value.

        Raises:
            ValueError: If min_val is greater than max_val.
        """
        if min_val > max_val:
            raise ValueError("Invalid range")
        return round(random.uniform(min_val, max_val), precision)

    @staticmethod
    def RandomInteger(min_val: int,
                      max_val: int) -> int:
        """
        Generate a random integer within a range.

        Uses random.randint (not secrets) as this is intended for non-security
        purposes (filter value randomization).

        Args:
            min_val: The minimum value (inclusive).
            max_val: The maximum value (inclusive).

        Returns:
            A random integer value.

        Raises:
            ValueError: If min_val is greater than max_val.
        """
        if min_val > max_val:
            raise ValueError("Invalid range")
        return random.randint(min_val, max_val)

    @staticmethod
    def RandomString(length: int) -> str:
        """
        Generate a random alphanumeric string.

        Args:
            length: The desired length of the string.

        Returns:
            A random string containing letters and digits.
        """
        return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


class Utils:
    """
    Provides general-purpose utility functions for type conversion and formatting.

    Offers string-to-type conversion methods (bool, int, float, lists, sets)
    and formatting utilities for output presentation.
    """

    @staticmethod
    def StrToBool(s: str) -> bool:
        """
        Convert a string to a boolean value.

        Args:
            s: The string to convert ('true', 'false', 'yes', 'no', etc.).

        Returns:
            The boolean value.

        Raises:
            ValueError: If the string cannot be converted to a boolean.
        """
        s = s.lower()
        if s in ["true", "on", "yes", "y"]:
            res = True
        elif s in ["false", "off", "no", "n"]:
            res = False
        else:
            raise ValueError("Invalid string")
        return res

    @staticmethod
    def StrToInt(s: str) -> int:
        """
        Convert a string to an integer.

        Args:
            s: The string to convert.

        Returns:
            The integer value.

        Raises:
            ValueError: If the string cannot be converted to an integer.
        """
        return int(s)

    @staticmethod
    def StrToFloat(s: str) -> float:
        """
        Convert a string to a float.

        Args:
            s: The string to convert.

        Returns:
            The float value.

        Raises:
            ValueError: If the string cannot be converted to a float.
        """
        return float(s)

    @staticmethod
    def IsStrInt(s: str) -> bool:
        """
        Check if a string represents an integer.

        Args:
            s: The string to check.

        Returns:
            True if the string is a valid integer, False otherwise.
        """
        try:
            Utils.StrToInt(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def IsStrFloat(s: str) -> bool:
        """
        Check if a string represents a float.

        Args:
            s: The string to check.

        Returns:
            True if the string is a valid float, False otherwise.
        """
        try:
            Utils.StrToFloat(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def StrToStrList(s: str) -> List[str]:
        """
        Convert a comma-separated string to a list of strings.

        Args:
            s: The comma-separated string.

        Returns:
            A list of trimmed strings, or empty list if input is empty.
        """
        return list(map(lambda v: v.strip(), s.split(","))) if s != "" else []
