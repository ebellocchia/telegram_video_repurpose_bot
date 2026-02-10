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
from pyrogram.types import InlineKeyboardMarkup
from typing_extensions import override

from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.ffmpeg.filter.filter_list import FilterList
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class ConfigFilterTypeSelectState(UserMenuStateBase):
    """Allows to select the filter to be configured."""

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
        Execute the configuration filter selection state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.BACK:
            return UserMenuStateTypes.CONFIG_FILTER_ACTION_SELECT
        if input_data == CallbackQueryTypes.START_MENU:
            return UserMenuStateTypes.CONFIG_MAIN_MENU

        filter_class = FilterList.GetByName(input_data)
        if filter_class:
            self._AddParams(user, config_filter_class=filter_class)
            # Go to toggle menu if toggle was selected
            if self._GetParam(user, UserMenuParams.CONFIG_FILTER_TOGGLE):
                return UserMenuStateTypes.CONFIG_FILTER_PARAM_TOGGLE
            # Otherwise, if filter has no named parameter, go directly to set value menu
            if not isinstance(filter_class.GetParametersInfo(), dict):
                self._AddParams(user, config_filter_param_name="", config_filter_param_set_err=False)
                return UserMenuStateTypes.CONFIG_FILTER_PARAM_SET_VALUE
            # If filter has named parameters, go to select parameter menu
            return UserMenuStateTypes.CONFIG_FILTER_PARAM_TYPE_SELECT
        return self._DefaultState()

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the filter selection menu to the user.

        Args:
            chat: The chat to display the menu in.
            user: The user viewing the menu.
        """
        buttons = []

        action_toggle = self._GetParam(user, UserMenuParams.CONFIG_FILTER_TOGGLE)
        filter_list = FilterList.GetByType(self._GetParam(user, UserMenuParams.CONFIG_FILTER_TYPE))
        for filter_class in filter_list:
            # If toggle, skip filters that cannot be enabled/disabled
            if action_toggle and not filter_class.GetEnabledFlag():
                continue
            # If set value, skip filters with no parameters
            if not action_toggle and not filter_class.GetParametersInfo():
                continue
            buttons.append([
                self.menu_btn_builder.KeyboardGenericButtonCbk(filter_class.Name())
            ])
        buttons.append([self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.BACK)])
        buttons.append([self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.START_MENU)])

        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("CONFIG_FILTER_SELECT_MSG"),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
