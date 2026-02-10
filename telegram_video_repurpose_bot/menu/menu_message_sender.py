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
from typing import Any, Dict, List

import pyrogram

from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.message.message_deleter import MessageDeleter
from telegram_video_repurpose_bot.message.message_editer import MessageEditer
from telegram_video_repurpose_bot.message.message_sender import MessageSender


@unique
class MenuMessageSenderTypes(Enum):
    """Menu message sender types."""
    SEND = auto()
    SEND_AND_ADD = auto()
    SEND_AND_DELETE = auto()
    SEND_AND_RESET = auto()
    SEND_AND_SET = auto()
    SEND_OR_EDIT = auto()


class MenuMessageSender:
    """
    Manages message lifecycle for menu interactions.

    Handles sending, editing, and deleting messages for menu displays with
    different strategies (add, replace, delete previous, send-or-edit).
    Tracks messages per user to manage state cleanup and message updates.
    """

    client: pyrogram.Client
    last_msgs: Dict[int, List[pyrogram.types.Message]]
    message_deleter: MessageDeleter
    message_editer: MessageEditer
    message_sender: MessageSender

    def __init__(self,
                 client: pyrogram.Client,
                 logger: Logger) -> None:
        """
        Initialize the menu message sender.

        Args:
            client: The Pyrogram client instance.
            logger: The logger instance.
        """
        self.client = client
        self.last_msgs = {}
        self.message_deleter = MessageDeleter(client, logger)
        self.message_editer = MessageEditer(client, logger)
        self.message_sender = MessageSender(client, logger)

    def ResetMessages(self,
                      user: pyrogram.types.User) -> None:
        """
        Reset messages for a user.

        Args:
            user: The user whose messages should be reset.
        """
        self.__ResetMessages(user)

    async def DeleteAllMessages(self,
                                user: pyrogram.types.User) -> None:
        """
        Delete all messages for a user.

        Args:
            user: The user whose messages should be deleted.
        """
        if user.id in self.last_msgs:
            await self.message_deleter.DeleteMessages(self.last_msgs[user.id])
            self.ResetMessages(user)

    def MessageCount(self,
                     user: pyrogram.types.User) -> int:
        """
        Get the count of messages for a user.

        Args:
            user: The user to get the message count for.

        Returns:
            The number of messages stored for the user.
        """
        self.__CreateUserIfNotExistent(user)
        return len(self.last_msgs[user.id])

    async def SendVideo(self,
                        msg_type: MenuMessageSenderTypes,
                        chat: pyrogram.types.Chat,
                        user: pyrogram.types.User,
                        video_file_name: str,
                        **kwargs: Any) -> None:
        """
        Send a video with specified message handling type.

        Args:
            msg_type: The type of message handling to use.
            chat: The chat to send the video to.
            user: The user sending the video.
            video_file_name: The file path of the video to send.
            **kwargs: Additional arguments to pass to the video sender.

        Raises:
            TypeError: If msg_type is not a MenuMessageSenderTypes enum.
            ValueError: If SEND_OR_EDIT is used with videos.
        """
        if not isinstance(msg_type, MenuMessageSenderTypes):
            raise TypeError("Message type shall be of MenuMessageSenderTypes enumerative")

        self.__CreateUserIfNotExistent(user)

        if msg_type == MenuMessageSenderTypes.SEND_OR_EDIT:
            raise ValueError("Send or edit not supported with photos")

        msg = await self.message_sender.SendVideo(chat, video_file_name, **kwargs)

        if msg_type == MenuMessageSenderTypes.SEND_AND_ADD and msg is not None:
            self.__AddMessages(user, [msg])
        elif msg_type == MenuMessageSenderTypes.SEND_AND_RESET:
            self.__ResetMessages(user)
        elif msg_type == MenuMessageSenderTypes.SEND_AND_SET and msg is not None:
            self.__SetMessages(user, [msg])
        elif msg_type == MenuMessageSenderTypes.SEND_AND_DELETE and msg is not None:
            await self.message_deleter.DeleteMessages(self.last_msgs[user.id])
            self.__SetMessages(user, [msg])

    async def SendMessage(self,
                          msg_type: MenuMessageSenderTypes,
                          chat: pyrogram.types.Chat,
                          user: pyrogram.types.User,
                          msg: str,
                          **kwargs: Any) -> None:
        """
        Send a message with specified message handling type.

        Args:
            msg_type: The type of message handling to use.
            chat: The chat to send the message to.
            user: The user sending the message.
            msg: The message content to send.
            **kwargs: Additional arguments to pass to the message sender.

        Raises:
            TypeError: If msg_type is not a MenuMessageSenderTypes enum.
        """
        if not isinstance(msg_type, MenuMessageSenderTypes):
            raise TypeError("Message type shall be of MenuMessageSenderTypes enumerative")

        self.__CreateUserIfNotExistent(user)

        if msg_type == MenuMessageSenderTypes.SEND_OR_EDIT:
            await self.__SendOrEditMessage(chat, user, msg, **kwargs)
        else:
            msgs = await self.message_sender.SendMessage(chat, msg, **kwargs)

            if msg_type == MenuMessageSenderTypes.SEND_AND_ADD:
                self.__AddMessages(user, msgs)
            elif msg_type == MenuMessageSenderTypes.SEND_AND_RESET:
                self.__ResetMessages(user)
            elif msg_type == MenuMessageSenderTypes.SEND_AND_SET:
                self.__SetMessages(user, msgs)
            elif msg_type == MenuMessageSenderTypes.SEND_AND_DELETE:
                await self.message_deleter.DeleteMessages(self.last_msgs[user.id])
                self.__SetMessages(user, msgs)

    def __AddMessages(self,
                      user: pyrogram.types.User,
                      msgs: List[pyrogram.types.Message]) -> None:
        """
        Add messages to the user's message list.

        Args:
            user: The user to add messages for.
            msgs: List of messages to add.
        """
        self.last_msgs[user.id].extend(msgs)

    def __ResetMessages(self,
                        user: pyrogram.types.User) -> None:
        """
        Clear all messages for a user.

        Args:
            user: The user whose messages should be cleared.
        """
        self.last_msgs[user.id] = []

    def __SetMessages(self,
                      user: pyrogram.types.User,
                      msgs: List[pyrogram.types.Message]) -> None:
        """
        Set the user's message list.

        Args:
            user: The user to set messages for.
            msgs: List of messages to set.
        """
        self.last_msgs[user.id] = msgs

    async def __SendOrEditMessage(self,
                                  chat: pyrogram.types.Chat,
                                  user: pyrogram.types.User,
                                  msg: str,
                                  **kwargs: Any) -> None:
        """
        Send a new message or edit the existing one.

        Args:
            chat: The chat to send or edit the message in.
            user: The user performing the action.
            msg: The message content.
            **kwargs: Additional arguments for the message sender.
        """
        if len(self.last_msgs[user.id]) == 0:
            msgs = await self.message_sender.SendMessage(chat, msg, **kwargs)
            self.__AddMessages(user, msgs)
        else:
            msgs = self.last_msgs[user.id]
            edited_msg = await self.__EditMessage(chat, msgs[0], msg, **kwargs)

            await self.message_deleter.DeleteMessages(msgs[1:])
            self.last_msgs[user.id] = [edited_msg]

    async def __EditMessage(self,
                            chat: pyrogram.types.Chat,
                            message: pyrogram.types.Message,
                            msg: str,
                            **kwargs: Any) -> pyrogram.types.Message:
        """
        Edit a message or send a new one if editing fails.

        Args:
            chat: The chat containing the message.
            message: The message to edit.
            msg: The new message content.
            **kwargs: Additional arguments for the message sender.

        Returns:
            The edited message or a newly sent message.
        """
        edited_msg = await self.message_editer.EditMessage(chat, message, msg, **kwargs)
        if edited_msg is None:
            edited_msg = (await self.message_sender.SendMessage(chat, msg, **kwargs))[0]

        return edited_msg

    def __CreateUserIfNotExistent(self,
                                  user: pyrogram.types.User) -> None:
        """
        Initialize message list for a user if not already done.

        Args:
            user: The user to initialize.
        """
        if user.id not in self.last_msgs:
            self.last_msgs[user.id] = []
