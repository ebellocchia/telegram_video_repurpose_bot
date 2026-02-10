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

from enum import Enum, auto, unique
from typing import Any

import pyrogram

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.message.message_deleter import MessageDeleter
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


@unique
class MessageTypes(Enum):
    """Message types."""
    GROUP_CHAT_CREATED = auto()
    LEFT_CHAT_MEMBER = auto()
    NEW_CHAT_MEMBERS = auto()
    PRIVATE = auto()


class MessageDispatcher:
    """
    Routes incoming Telegram messages to appropriate handlers.

    Dispatches messages based on type (private, group chat, member changes)
    to the correct handler methods for processing different message categories.
    """

    config: ConfigObject
    logger: Logger
    translator: TranslationLoader

    def __init__(self,
                 config: ConfigObject,
                 logger: Logger,
                 translator: TranslationLoader) -> None:
        """
        Initialize the message dispatcher.

        Args:
            config: Configuration object.
            logger: The logger instance.
            translator: The translation loader instance.
        """
        self.config = config
        self.logger = logger
        self.translator = translator

    async def Dispatch(self,
                       client: pyrogram.Client,
                       message: pyrogram.types.Message,
                       msg_type: MessageTypes,
                       **kwargs: Any) -> None:
        """
        Dispatch a message to the appropriate handler based on message type.

        Args:
            client: The Pyrogram client instance.
            message: The incoming message.
            msg_type: The type of message being dispatched.
            **kwargs: Additional arguments to pass to handlers.

        Raises:
            TypeError: If msg_type is not a MessageTypes enum.
        """
        if not isinstance(msg_type, MessageTypes):
            raise TypeError("Message type is not an enumerative of MessageTypes")

        self.logger.GetLogger().info(f"Dispatching message type: {msg_type}")

        try:
            if msg_type == MessageTypes.GROUP_CHAT_CREATED:
                await self.__OnCreatedChat(client, message, **kwargs)
            elif msg_type == MessageTypes.LEFT_CHAT_MEMBER:
                await self.__OnLeftMember(client, message, **kwargs)
            elif msg_type == MessageTypes.NEW_CHAT_MEMBERS:
                await self.__OnJoinedMember(client, message, **kwargs)
            elif msg_type == MessageTypes.PRIVATE:
                await self.__OnPrivateMessage(client, message, **kwargs)
        except Exception:
            raise

    async def __OnCreatedChat(self,
                              client,
                              message: pyrogram.types.Message,
                              **kwargs: Any) -> None:
        """
        Handle group chat creation event.

        Args:
            client: The Pyrogram client instance.
            message: The message indicating chat creation.
            **kwargs: Additional handler arguments.
        """
        if message.chat is None:
            return

    async def __OnLeftMember(self,
                             client,
                             message: pyrogram.types.Message,
                             **kwargs: Any) -> None:
        """
        Handle member left chat event.

        Args:
            client: The Pyrogram client instance.
            message: The message indicating member departure.
            **kwargs: Additional handler arguments.
        """
        if message.left_chat_member is not None and message.left_chat_member.is_self:
            pass

    async def __OnJoinedMember(self,
                               client,
                               message: pyrogram.types.Message,
                               **kwargs: Any) -> None:
        """
        Handle member joined chat event.

        Args:
            client: The Pyrogram client instance.
            message: The message indicating member joining.
            **kwargs: Additional handler arguments.
        """
        if message.new_chat_members is None or message.chat is None:
            return

    async def __OnPrivateMessage(self,
                                 client,
                                 message: pyrogram.types.Message,
                                 **kwargs: Any) -> None:
        """
        Handle private message received event.

        Args:
            client: The Pyrogram client instance.
            message: The private message received.
            **kwargs: Additional handler arguments including 'user_menu'.
        """
        if message.chat is None or message.from_user is None:
            return

        if message.video is not None:
            msg_text = await message.download(
                file_name=self.config.GetValue(BotConfigTypes.VIDEO_DOWNLOAD_FOLDER)
            )
        else:
            msg_text = message.text

        await MessageDeleter(client, self.logger).DeleteMessage(message)
        await kwargs["user_menu"].OnMessage(message.chat, message.from_user, msg_text)
