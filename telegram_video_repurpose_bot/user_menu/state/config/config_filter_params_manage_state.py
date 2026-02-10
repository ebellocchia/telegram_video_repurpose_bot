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
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_types import FfmpegConfigTypes
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase, UserMenuStateBaseInitParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class ConfigFilterParamsManageState(UserMenuStateBase):
    """Allows to manage filter parameters."""

    ffmpeg_config_mgr: FfmpegConfigManager

    def __init__(self,
                 params: UserMenuStateBaseInitParams) -> None:
        """
        Initialize the filter parameter management state.

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
        Execute the configuration filter parameters management state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.BACK:
            return UserMenuStateTypes.CONFIG_MAIN_MENU
        if input_data == CallbackQueryTypes.CONFIG_LOAD_PARAMS:
            self.ffmpeg_config_mgr.LoadConfig()
            return self._ResultState(
                user,
                "CONFIG_PARAMS_LOADED_MSG",
                back_state = UserMenuStateTypes.CONFIG_FILTER_PARAMS_MANAGE
            )
        if input_data == CallbackQueryTypes.CONFIG_SAVE_PARAMS:
            self.ffmpeg_config_mgr.SaveConfig()
            return self._ResultState(
                user,
                "CONFIG_PARAMS_SAVED_MSG",
                back_state=UserMenuStateTypes.CONFIG_FILTER_PARAMS_MANAGE
            )
        if input_data == CallbackQueryTypes.CONFIG_SHOW_PARAMS:
            params_str = self.__GetParamsString()
            return self._ResultState(
                user,
                "CONFIG_PARAMS_SHOW_MSG",
                back_state=UserMenuStateTypes.CONFIG_FILTER_PARAMS_MANAGE,
                params_str=params_str
            )

        return self._DefaultState()

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the filter parameters management menu to the user.

        Args:
            chat: The chat to display the menu in.
            user: The user viewing the menu.
        """
        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("CONFIG_PARAMS_MANAGE_MSG"),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.CONFIG_LOAD_PARAMS)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.CONFIG_SAVE_PARAMS)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.CONFIG_SHOW_PARAMS)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.BACK)
                    ],
                ]
            )
        )

    def __GetParamsString(self) -> str:
        """
        Get the string with status of all FFmpeg parameters.

        Returns:
            Parameters status string.
        """
        params_str = []
        ffmpeg_config = self.ffmpeg_config_mgr.GetConfig()
        for config_type in FfmpegConfigTypes:
            name = config_type.name.lower().replace("ffmpeg_", "")
            params_str.append(f"• {name}: {ffmpeg_config.GetValue(config_type)}")
        return "\n".join(params_str)
