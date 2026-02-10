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

from typing import Any, Dict


class KeyValueConverter:
    """
    Bidirectional conversion between dictionary keys and values.

    Allows looking up values by key and keys by value in a dictionary,
    providing two-way mapping capabilities.
    """

    kv_dict: Dict[str, Any]

    def __init__(self,
                 kv_dict: Dict[str, Any]) -> None:
        """
        Initialize the key-value converter.

        Args:
            kv_dict: Dictionary mapping keys to values.
        """
        self.kv_dict = kv_dict

    def KeyToValue(self,
                   key: str) -> Any:
        """
        Convert a key to its corresponding value.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key.
        """
        return self.kv_dict[key]

    def ValueToKey(self,
                   value: Any) -> str:
        """
        Convert a value to its corresponding key.

        Args:
            value: The value to look up.

        Returns:
            The key associated with the value.
        """
        idx = list(self.kv_dict.values()).index(value)
        return list(self.kv_dict.keys())[idx]
