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

from typing import Any, Optional

import pyrogram
import pyrogram.errors.exceptions as pyrogram_ex

from telegram_video_repurpose_bot.logger.logger import Logger


class MessageEditer:
    """
    Edits message text content in Telegram chats.

    Modifies existing message text with error handling for invalid or
    unmodifiable messages, returning the edited message or None on failure.
    """

    client: pyrogram.Client
    logger: Logger

    def __init__(self,
                 client: pyrogram.Client,
                 logger: Logger) -> None:
        """
        Initialize the message editer.

        Args:
            client: The Pyrogram client instance.
            logger: The logger instance.
        """
        self.client = client
        self.logger = logger

    async def EditMessage(self,
                          chat: pyrogram.types.Chat,
                          message: pyrogram.types.Message,
                          msg: str,
                          **kwargs: Any) -> Optional[pyrogram.types.Message]:
        """
        Edit a message's text content.

        Args:
            chat: The chat containing the message.
            message: The message to edit.
            msg: The new message text.
            **kwargs: Additional arguments for the edit_message_text method.

        Returns:
            The edited message object or None if editing failed.
        """
        try:
            return await self.client.edit_message_text(chat.id, message.id, msg, **kwargs)
        except pyrogram_ex.bad_request_400.MessageIdInvalid:
            self.logger.GetLogger().exception(f"Unable to modify message {message.id}")
            return None
        except pyrogram_ex.bad_request_400.MessageNotModified:
            return message
