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
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_manager import FfmpegConfigManager
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase, UserMenuStateBaseInitParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class ConfigFilterParamToggleValueState(UserMenuStateBase):
    """Allows to toggle a filter parameter."""

    ffmpeg_config_mgr: FfmpegConfigManager

    def __init__(self,
                 params: UserMenuStateBaseInitParams) -> None:
        """
        Initialize the toggle filter parameter set state.

        Args:
            params: UserMenuStateBaseInitParams containing initialization parameters.
        """
        super().__init__(params)
        self.ffmpeg_config_mgr = params.ffmpeg_config_mgr

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
        Execute the configuration filter parameter set state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.BACK:
            return UserMenuStateTypes.CONFIG_FILTER_TYPE_SELECT

        ffmpeg_config = self.ffmpeg_config_mgr.GetConfig()
        filter_class = self._GetParam(user, UserMenuParams.CONFIG_FILTER_CLASS)
        # Enable button
        if input_data == CallbackQueryTypes.CONFIG_FILTER_ENABLE:
            ffmpeg_config.SetValue(filter_class.GetEnabledFlag(), True)
            return UserMenuStateTypes.CONFIG_FILTER_PARAM_TOGGLE
        # Disable button
        if input_data == CallbackQueryTypes.CONFIG_FILTER_DISABLE:
            ffmpeg_config.SetValue(filter_class.GetEnabledFlag(), False)
            return UserMenuStateTypes.CONFIG_FILTER_PARAM_TOGGLE

        return self._DefaultState()

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the filter parameter set menu to the user.

        Args:
            chat: The chat to display the menu in.
            user: The user viewing the menu.
        """
        filter_class = self._GetParam(user, UserMenuParams.CONFIG_FILTER_CLASS)
        is_enabled = filter_class(self.ffmpeg_config_mgr.GetConfig()).IsEnabled()

        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("CONFIG_FILTER_PARAM_TOGGLE_MSG",
                                        curr_status=(self.translator.GetSentence("ENABLED_MSG")
                                                     if is_enabled else
                                                     self.translator.GetSentence("DISABLED_MSG")),
                                        filter_name=filter_class.Name()),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.CONFIG_FILTER_ENABLE)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.CONFIG_FILTER_DISABLE)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.BACK)
                    ],
                ]
            )
        )
