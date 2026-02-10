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
from typing_extensions import override

from telegram_video_repurpose_bot.app.app_users import AppUsers
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class ConfigInitState(UserMenuStateBase):
    """
    Initializes the configuration by checking user authorization.

    Validates user permissions before showing available configuration menu,
    transitioning to the configuration menu state or showing an error.
    """

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            False, as this is an initialization state that doesn't wait for input.
        """
        return False

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the configuration initialization logic.

        Args:
            user: The user executing the state.
            input_data: Input data from user interaction.

        Returns:
            The next menu state type (configuration main menu state if authorized).
        """
        if not AppUsers(self.bot_config).IsAuthorized(user):
            return self._ResultState(user, "USER_AUTH_CMD_ERR_MSG")
        return UserMenuStateTypes.CONFIG_MAIN_MENU

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the configuration initialization (nothing displayed).

        Args:
            chat: The chat to display content in.
            user: The user viewing the state.
        """
        pass
