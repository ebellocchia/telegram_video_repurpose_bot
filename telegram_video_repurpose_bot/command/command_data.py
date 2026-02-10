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

from typing import Any, Callable, List, Optional, Set, Union

import pyrogram

from telegram_video_repurpose_bot.utils.utils import Utils
from telegram_video_repurpose_bot.utils.wrapped_list import WrappedList


class CommandParameterError(Exception):
    """Exception raised when a command parameter is invalid."""


class CommandParametersList(WrappedList):
    """Class for managing command parameters list."""

    def GetAsBool(self,
                  idx: int,
                  def_val: Optional[bool] = None) -> bool:
        """
        Get parameter as bool.

        Args:
            idx: Parameter index.
            def_val: Default value.

        Returns:
            bool: Parameter value.
        """
        return self.__GetGenericParam(Utils.StrToBool, idx, def_val)

    def GetAsFloat(self,
                   idx: int,
                   def_val: Optional[float] = None) -> float:
        """
        Get parameter as float.

        Args:
            idx: Parameter index.
            def_val: Default value.

        Returns:
            float: Parameter value.
        """
        return self.__GetGenericParam(Utils.StrToFloat, idx, def_val)

    def GetAsInt(self,
                 idx: int,
                 def_val: Optional[int] = None) -> int:
        """
        Get parameter as int.

        Args:
            idx: Parameter index.
            def_val: Default value.

        Returns:
            int: Parameter value.
        """
        return self.__GetGenericParam(Utils.StrToInt, idx, def_val)

    def GetAsString(self,
                    idx: int,
                    def_val: Optional[str] = None) -> str:
        """
        Get parameter as string.

        Args:
            idx: Parameter index.
            def_val: Default value.

        Returns:
            str: Parameter value.
        """
        return self.__GetGenericParam(str, idx, def_val)

    def GetAsList(self,
                  start_idx: int) -> List[str]:
        """
        Get parameters as list.

        Args:
            start_idx: Start index.

        Returns:
            List[str]: List of parameter values.
        """
        list_val = []

        idx = start_idx
        finished = False
        while not finished:
            try:
                part = self.GetAsString(idx)
            except CommandParameterError:
                finished = True
            else:
                list_val.extend(part.strip(", ").split(","))
                idx += 1

        return list_val

    def GetAsSet(self,
                 start_idx: int) -> Set[str]:
        """
        Get parameters as set.

        Args:
            start_idx: Start index.

        Returns:
            Set[str]: Set of parameter values.
        """
        return set(self.GetAsList(start_idx))

    def IsLast(self,
               value: Union[int, str]) -> bool:
        """
        Check if last parameter is the specified value.

        Args:
            value: Value to check.

        Returns:
            bool: True if last parameter matches value, False otherwise.
        """
        try:
            return value == self.list_elements[self.Count() - 1]
        except IndexError:
            return False

    def IsValue(self,
                value: Union[int, str]) -> bool:
        """
        Check if value is present.

        Args:
            value: Value to check.

        Returns:
            bool: True if value is present, False otherwise.
        """
        return value in self.list_elements

    def __GetGenericParam(self,
                          conv_fct: Callable[[str], Any],
                          idx: int,
                          def_val: Optional[Any]) -> Any:
        """
        Get generic parameter.

        Args:
            conv_fct: Conversion function.
            idx: Parameter index.
            def_val: Default value.

        Returns:
            Any: Parameter value.
        """
        try:
            return conv_fct(self.list_elements[idx])
        except (ValueError, IndexError) as ex:
            if def_val is not None:
                return def_val
            raise CommandParameterError(f"Invalid command parameter #{idx}") from ex


class CommandData:
    """Class for storing command data."""

    cmd_name: str
    cmd_params: CommandParametersList
    cmd_chat: pyrogram.types.Chat
    cmd_user: Optional[pyrogram.types.User]

    def __init__(self,
                 message: pyrogram.types.Message) -> None:
        """
        Construct class.

        Args:
            message: Pyrogram message object.
        """
        if message.command is None or message.chat is None:
            raise ValueError("Invalid command")

        self.cmd_name = message.command[0]
        self.cmd_params = CommandParametersList()
        self.cmd_params.AddMultiple(message.command[1:])
        self.cmd_chat = message.chat
        self.cmd_user = message.from_user

    def Name(self) -> str:
        """
        Get command name.

        Returns:
            str: Command name.
        """
        return self.cmd_name

    def Chat(self) -> pyrogram.types.Chat:
        """
        Get chat.

        Returns:
            pyrogram.types.Chat: Chat object.
        """
        return self.cmd_chat

    def User(self) -> Optional[pyrogram.types.User]:
        """
        Get user.

        Returns:
            Optional[pyrogram.types.User]: User object or None.
        """
        return self.cmd_user

    def Params(self) -> CommandParametersList:
        """
        Get parameters.

        Returns:
            CommandParametersList: Parameters list.
        """
        return self.cmd_params
