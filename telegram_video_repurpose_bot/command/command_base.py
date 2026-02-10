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
from typing import Any

import pyrogram
from pyrogram.errors import RPCError

from telegram_video_repurpose_bot.command.command_data import CommandData
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.message.message_sender import MessageSender
from telegram_video_repurpose_bot.misc.helpers import ChatHelper, UserHelper
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


class CommandBase(ABC):
    """Abstract base class for commands."""

    client: pyrogram.Client
    config: ConfigObject
    logger: Logger
    translator: TranslationLoader
    message: pyrogram.types.Message
    cmd_data: CommandData
    message_sender: MessageSender

    def __init__(self,
                 client: pyrogram.Client,
                 config: ConfigObject,
                 logger: Logger,
                 translator: TranslationLoader) -> None:
        """
        Construct class.

        Args:
            client: Pyrogram client
            config: Configuration object
            logger: Logger instance
            translator: Translation loader
        """
        self.client = client
        self.config = config
        self.logger = logger
        self.translator = translator
        self.message_sender = MessageSender(client, logger)

    async def Execute(self,
                      message: pyrogram.types.Message,
                      **kwargs: Any) -> None:
        """
        Execute command.

        Args:
            message: Pyrogram message object
            **kwargs: Additional keyword arguments
        """
        self.message = message
        self.cmd_data = CommandData(message)

        self.__LogCommand()

        if self._IsUserAnonymous():
            self.logger.GetLogger().warning("An anonymous user tried to execute the command, exiting")
            return

        try:
            await self._ExecuteCommand(**kwargs)
        except RPCError:
            await self._SendMessage(self.translator.GetSentence("CMD_GENERIC_ERR_MSG"))
            self.logger.GetLogger().exception(
                f"An error occurred while executing command {self.cmd_data.Name()}"
            )

    async def _SendMessage(self,
                           msg: str) -> None:
        """
        Send message.

        Args:
            msg: Message to send
        """
        await self.message_sender.SendMessage(self.cmd_data.Chat(), msg)

    def _IsUserAnonymous(self) -> bool:
        """
        Get if user is anonymous.

        Returns:
            bool: True if user is anonymous, False otherwise
        """
        return self.cmd_data.User() is None

    def _IsPrivateChat(self) -> bool:
        """
        Get if chat is private.

        Returns:
            bool: True if chat is private, False otherwise
        """
        cmd_user = self.cmd_data.User()
        if cmd_user is None:
            return False
        return ChatHelper.IsPrivateChat(self.cmd_data.Chat(), cmd_user)

    def __LogCommand(self) -> None:
        """Log command execution."""
        self.logger.GetLogger().info(f"Command: {self.cmd_data.Name()}")
        self.logger.GetLogger().info(f"Executed by user: {UserHelper.GetNameOrId(self.cmd_data.User())}")
        self.logger.GetLogger().debug(f"Received message: {self.message}")

    @abstractmethod
    async def _ExecuteCommand(self,
                              **kwargs: Any) -> None:
        """
        Execute command implementation.

        Args:
            **kwargs: Additional keyword arguments
        """
