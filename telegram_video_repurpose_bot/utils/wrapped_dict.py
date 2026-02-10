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

import typing
from abc import ABC
from collections.abc import ItemsView, KeysView, ValuesView
from typing import Dict, Iterator, Optional


class WrappedDict(ABC):
    """
    Abstract wrapper class for dictionary operations and queries.

    Provides a simplified interface for common dictionary operations including
    adding/removing elements, querying keys/values, and managing dictionary state.
    """

    dict_elements: Dict[typing.Any, typing.Any]

    def __init__(self) -> None:
        """Initialize the wrapped dictionary."""
        self.dict_elements = {}

    def AddSingle(self,
                  key: typing.Any,
                  value: typing.Any) -> None:
        """
        Add a single key-value pair.

        Args:
            key: The key to add.
            value: The value associated with the key.
        """
        self.dict_elements[key] = value

    def AddMultiple(self,
                    elements: Dict[typing.Any, typing.Any]) -> None:
        """
        Add multiple key-value pairs.

        Args:
            elements: Dictionary of key-value pairs to add.
        """
        self.dict_elements = {**self.dict_elements, **elements}

    def RemoveSingle(self,
                     key: typing.Any) -> typing.Any:
        """
        Remove a key-value pair by key.

        Args:
            key: The key to remove.

        Returns:
            The value associated with the key, or None if key doesn't exist.
        """
        return self.dict_elements.pop(key, None)

    def IsKey(self,
              key: typing.Any) -> bool:
        """
        Check if a key exists in the dictionary.

        Args:
            key: The key to check.

        Returns:
            True if the key exists, False otherwise.
        """
        return key in self.dict_elements

    def IsValue(self,
                value: typing.Any) -> bool:
        """
        Check if a value exists in the dictionary.

        Args:
            value: The value to check.

        Returns:
            True if the value exists, False otherwise.
        """
        return value in self.dict_elements.values()

    def Keys(self) -> KeysView:
        """
        Get all keys in the dictionary.

        Returns:
            A KeysView of the dictionary's keys.
        """
        return self.dict_elements.keys()

    def Values(self) -> ValuesView:
        """
        Get all values in the dictionary.

        Returns:
            A ValuesView of the dictionary's values.
        """
        return self.dict_elements.values()

    def Items(self) -> ItemsView:
        """
        Get all key-value pairs in the dictionary.

        Returns:
            An ItemsView of the dictionary's items.
        """
        return self.dict_elements.items()

    def Get(self,
            key: typing.Any,
            def_val: Optional[typing.Any]) -> Optional[typing.Any]:
        """
        Get a value by key with a default value.

        Args:
            key: The key to look up.
            def_val: The default value if key doesn't exist.

        Returns:
            The value for the key or the default value.
        """
        return self.dict_elements.get(key, def_val)

    def Clear(self) -> None:
        """Clear all elements from the dictionary."""
        self.dict_elements.clear()

    def Count(self) -> int:
        """
        Get the count of key-value pairs in the dictionary.

        Returns:
            The number of pairs in the dictionary.
        """
        return len(self.dict_elements)

    def Any(self) -> bool:
        """
        Check if the dictionary contains any elements.

        Returns:
            True if the dictionary is not empty, False otherwise.
        """
        return self.Count() > 0

    def Empty(self) -> bool:
        """
        Check if the dictionary is empty.

        Returns:
            True if the dictionary is empty, False otherwise.
        """
        return self.Count() == 0

    def GetDict(self) -> Dict[typing.Any, typing.Any]:
        """
        Get the underlying dictionary.

        Returns:
            The dictionary of elements.
        """
        return self.dict_elements

    def __getitem__(self,
                    key: typing.Any):
        """
        Get an item by key using bracket notation.

        Args:
            key: The key to look up.

        Returns:
            The value for the key.
        """
        return self.dict_elements[key]

    def __delitem__(self,
                    key: typing.Any):
        """
        Delete an item by key using bracket notation.

        Args:
            key: The key to delete.
        """
        del self.dict_elements[key]

    def __setitem__(self,
                    key: typing.Any,
                    value: typing.Any):
        """
        Set an item by key using bracket notation.

        Args:
            key: The key to set.
            value: The value to set.
        """
        self.dict_elements[key] = value

    def __iter__(self) -> Iterator[typing.Any]:
        """
        Get an iterator for the dictionary keys.

        Returns:
            An iterator over the dictionary keys.
        """
        yield from self.dict_elements

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns:
            String representation of the dictionary.
        """
        return str(self.dict_elements)
