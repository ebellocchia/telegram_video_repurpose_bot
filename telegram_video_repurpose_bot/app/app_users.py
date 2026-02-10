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

import pyrogram

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.config.config_object import ConfigObject


class AppUsers:
    """Class for managing application users and their permissions."""

    config: ConfigObject

    def __init__(self,
                 config: ConfigObject) -> None:
        """
        Construct class.

        Args:
            config: Configuration object
        """
        self.config = config

    def IsAdmin(self,
                user: pyrogram.types.User) -> bool:
        """
        Get if user is admin.

        Args:
            user: User object

        Returns:
            bool: True if the user is an admin, False otherwise
        """
        if user.username is None:
            return False
        return user.username.lower() in self.config.GetValue(BotConfigTypes.APP_ADMIN_USERS)

    def IsAuthorized(self,
                     user: pyrogram.types.User) -> bool:
        """
        Get if user is authorized.

        Args:
            user: User object

        Returns:
            bool: True if the user is authorized, False otherwise
        """
        if user.username is None:
            return False
        return self.IsAdmin(user) or user.username.lower() in self.config.GetValue(BotConfigTypes.APP_AUTH_USERS)
