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

from typing import Dict

import pyrogram
from pyrogram.types import InlineKeyboardMarkup
from typing_extensions import override

from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.misc.helpers import UserHelper
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class StartMenuStateConst:
    """Constants for start menu state class."""
    # Next states map
    NEXT_STATES_MAP: Dict[str, MenuStateTypes] = {
        CallbackQueryTypes.CONFIG_MAIN_MENU: UserMenuStateTypes.CONFIG_MAIN_MENU,
        CallbackQueryTypes.INFO_BOT: UserMenuStateTypes.INFO_BOT,
        CallbackQueryTypes.REPURPOSE_VIDEO: UserMenuStateTypes.REPURPOSE_VIDEO_INIT,
    }


class StartMenuState(UserMenuStateBase):
    """
    Displays the main menu with navigation options.

    Shows the primary menu interface with buttons for video processing,
    commands, and bot information. Handles transitions to corresponding states.
    """

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True, as the start menu waits for user input.
        """
        return True

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the start menu state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        self.state_params.ClearByUser(user)
        return StartMenuStateConst.NEXT_STATES_MAP.get(input_data, self._DefaultState())

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the start menu to the user.

        Args:
            chat: The chat to display the menu in.
            user: The user viewing the menu.
        """
        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("START_MENU_MSG",
                                        name=UserHelper.GetName(user)),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.REPURPOSE_VIDEO)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.CONFIG_MAIN_MENU)
                    ],
                    [
                        self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.INFO_BOT)
                    ]
                ]
            )
        )
