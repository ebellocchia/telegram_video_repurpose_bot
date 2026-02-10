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

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.misc.helpers import UserHelper
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class ConfigBotAccessAddState(UserMenuStateBase):
    """Allows to add new authorized users to bot access."""

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True, the state waits for user input.
        """
        return True

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the configuration bot access add state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.BACK:
            return UserMenuStateTypes.CONFIG_BOT_ACCESS
        if not all(UserHelper.IsValidUsername(username) for username in input_data.split()):
            return self._ResultState(
                user,
                "CONFIG_BOT_ACCESS_INPUT_ERR_MSG",
                back_state=UserMenuStateTypes.CONFIG_BOT_ACCESS
            )

        self.__UpdateAuthorizedUsers(input_data)
        return self._ResultState(
            user,
            "CONFIG_BOT_ACCESS_ADDED_MSG",
            back_state=UserMenuStateTypes.CONFIG_BOT_ACCESS
        )

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the bot access add menu to the user.

        Args:
            chat: The chat to display the menu in.
            user: The user viewing the menu.
        """
        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("CONFIG_BOT_ACCESS_ADD_MSG"),
            reply_markup=self.menu_btn_builder.KeyboardMarkupCbk(UserMenuBtnTypes.BACK)
        )

    def __UpdateAuthorizedUsers(self,
                                input_data: str) -> None:
        """
        Update the authorized users by adding new usernames.

        It also saves the bot configuration to file.

        Args:
            input_data: Input data from user.
        """
        usernames = set(
            UserHelper.CleanUsername(username) for username in input_data.split()
        )
        auth_users = self.bot_config.GetValue(BotConfigTypes.APP_AUTH_USERS)
        auth_users.update(usernames)
        self.bot_config.SetValue(BotConfigTypes.APP_AUTH_USERS, auth_users)

        self.bot_config_mgr.SaveConfig(self.logger)
