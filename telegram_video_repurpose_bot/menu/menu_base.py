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

from abc import ABC, abstractmethod
from typing import Dict

import pyrogram

from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSender
from telegram_video_repurpose_bot.menu.menu_state_base import MenuStateBase
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.misc.helpers import UserHelper


class MenuBase(ABC):
    """
    Abstract base class for Telegram menus with state machine architecture.

    Provides core menu functionality including state management, message handling,
    callback processing, and transitions between menu states. Requires subclasses
    to implement initial state and close query detection.
    """

    logger: Logger
    menu_message_sender: MenuMessageSender
    menu_states_obj: Dict[MenuStateTypes, MenuStateBase]
    menu_states: Dict[int, MenuStateBase]

    def __init__(self,
                 client: pyrogram.Client,
                 logger: Logger) -> None:
        """
        Initialize the menu base.

        Args:
            client: The Pyrogram client instance.
            logger: The logger instance.
        """
        self.logger = logger
        self.menu_message_sender = MenuMessageSender(client, logger)
        self.menu_states_obj = {}
        self.menu_states = {}

    def IsClosed(self,
                 user: pyrogram.types.User) -> bool:
        """
        Check if the menu is closed for a user.

        Args:
            user: The user to check.

        Returns:
            True if the menu is closed, False otherwise.
        """
        return self.menu_message_sender.MessageCount(user) == 0

    async def Close(self,
                    user: pyrogram.types.User) -> None:
        """
        Close the menu for a user.

        Args:
            user: The user whose menu should be closed.
        """
        self.logger.GetLogger().info(
            f"Closing menu {self.__MenuName()} for user {UserHelper.GetNameOrId(user)}"
        )

        self.__ResetUserState(user)
        await self.menu_message_sender.DeleteAllMessages(user)

    async def Reset(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Reset the menu to its initial state.

        Args:
            chat: The chat where the menu is displayed.
            user: The user whose menu should be reset.
        """
        await self.Close(user)
        await self.__ExecuteState(chat, user, "")

    async def OnCallback(self,
                         chat: pyrogram.types.Chat,
                         user: pyrogram.types.User,
                         cbk_data: str) -> None:
        """
        Handle callback data from a button click.

        Args:
            chat: The chat where the callback originated.
            user: The user who clicked the button.
            cbk_data: The callback data from the button.
        """
        if self._IsCloseQuery(cbk_data):
            await self.Close(user)
        else:
            await self.__ExecuteState(chat, user, cbk_data)

    async def OnMessage(self,
                        chat: pyrogram.types.Chat,
                        user: pyrogram.types.User,
                        message: str) -> None:
        """
        Handle incoming message from user.

        Args:
            chat: The chat where the message originated.
            user: The user who sent the message.
            message: The message content.
        """
        await self.__ExecuteState(chat, user, message)

    async def __ExecuteState(self,
                             chat: pyrogram.types.Chat,
                             user: pyrogram.types.User,
                             input_data: str) -> None:
        """
        Execute menu state and handle transitions.

        Args:
            chat: The chat for displaying menu output.
            user: The user executing the menu.
            input_data: Input data from callback or message.
        """
        input_data = input_data.strip()

        self.logger.GetLogger().info(
            f"Executing menu {self.__MenuName()} for user {UserHelper.GetNameOrId(user)}, input_data: {input_data}"
        )

        curr_state = self.menu_states.get(user.id,
                                          self.menu_states_obj[self._InitMenuState()])

        while True:
            next_state = self.menu_states_obj[await curr_state.Execute(user, input_data)]
            await next_state.Show(chat, user)
            curr_state = next_state
            if curr_state.WaitsForInput():
                break
        self.menu_states[user.id] = curr_state

    def __MenuName(self) -> str:
        """
        Get the menu class name.

        Returns:
            The class name of the menu.
        """
        return self.__class__.__name__

    def __ResetUserState(self,
                         user: pyrogram.types.User) -> None:
        """
        Reset user's menu state to initial state.

        Args:
            user: The user whose state should be reset.
        """
        self.menu_states[user.id] = self.menu_states_obj[self._InitMenuState()]

    @staticmethod
    @abstractmethod
    def _IsCloseQuery(cbk_data: str) -> bool:
        """
        Check if callback data represents a close query.

        Args:
            cbk_data: The callback data to check.

        Returns:
            True if the callback is a close query, False otherwise.
        """

    @abstractmethod
    def _InitMenuState(self) -> MenuStateTypes:
        """
        Get the initial menu state type.

        Returns:
            The MenuStateTypes value for the initial state.
        """
