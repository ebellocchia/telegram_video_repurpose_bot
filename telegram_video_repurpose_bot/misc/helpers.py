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

import re
from typing import Optional

import pyrogram
from pyrogram.enums import ChatType


class ChatHelper:
    """Utility methods for chat-related operations."""

    @staticmethod
    def IsChannel(chat: pyrogram.types.Chat) -> bool:
        """
        Check if a chat is a channel.

        Args:
            chat: The chat to check.

        Returns:
            True if the chat is a channel, False otherwise.
        """
        return chat.type == ChatType.CHANNEL

    @staticmethod
    def GetTitle(chat: pyrogram.types.Chat) -> str:
        """
        Get the title of a chat.

        Args:
            chat: The chat to get the title from.

        Returns:
            The chat title or empty string if not available.
        """
        return chat.title if chat.title is not None else ""

    @staticmethod
    def GetTitleOrId(chat: pyrogram.types.Chat) -> str:
        """
        Get the chat title or ID as a formatted string.

        Args:
            chat: The chat to get information from.

        Returns:
            Formatted string with title and ID or just the ID.
        """
        return f"'{chat.title}' (ID: {chat.id})" if chat.title is not None else f"{chat.id}"

    @staticmethod
    def IsPrivateChat(chat: pyrogram.types.Chat,
                      user: pyrogram.types.User) -> bool:
        """
        Check if a chat is a private chat with a specific user.

        Args:
            chat: The chat to check.
            user: The user to check against.

        Returns:
            True if the chat is a private chat with the user, False otherwise.
        """
        if ChatHelper.IsChannel(chat):
            return False
        return chat.id == user.id


class UserHelper:
    """Utility methods for user-related operations."""

    @staticmethod
    def IsValidUsername(username: str) -> bool:
        """
        Check if a username is valid.

        Args:
            username: The username string, may include '@' prefix.

        Returns:
            True if the username is valid, False otherwise.
        """
        username = UserHelper.CleanUsername(username)
        return re.match(r"^[a-zA-Z_][a-zA-Z0-9_]{4,31}$", username) is not None

    @staticmethod
    def CleanUsername(username: str) -> str:
        """
        Get username without the '@' prefix if present.

        Args:
            username: The username string, may include '@' prefix.

        Returns:
            The username without the '@' prefix.
        """
        return username[1:].lower() if username.startswith("@") else username.lower()

    @staticmethod
    def GetNameOrId(user: Optional[pyrogram.types.User]) -> str:
        """
        Get a formatted string with user name or ID.

        Args:
            user: The user object, or None for anonymous user.

        Returns:
            Formatted string with user information including username, name, and ID.
        """
        if user is None:
            return "Anonymous user"

        if user.username is not None:
            return f"@{user.username} ({UserHelper.GetName(user)} - ID: {user.id})"

        name = UserHelper.GetName(user)
        return f"{name} (ID: {user.id})" if name is not None else f"ID: {user.id}"

    @staticmethod
    def GetName(user: Optional[pyrogram.types.User]) -> str:
        """
        Get the full name of a user.

        Args:
            user: The user object, or None for anonymous user.

        Returns:
            The user's full name or empty string if not available.
        """
        if user is None:
            return "Anonymous user"

        if user.first_name is not None:
            return f"{user.first_name} {user.last_name}" if user.last_name is not None else f"{user.first_name}"
        return user.last_name if user.last_name is not None else ""
