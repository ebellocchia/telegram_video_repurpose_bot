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
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class RepurposeVideoCompletedConst:
    """Constants for repurpose video completed state class."""
    # Next states map
    NEXT_STATES_MAP: Dict[str, MenuStateTypes] = {
        CallbackQueryTypes.REPURPOSE_VIDEO: UserMenuStateTypes.REPURPOSE_VIDEO_INIT,
        CallbackQueryTypes.START_MENU: UserMenuStateTypes.START_MENU,
    }


class RepurposeVideoCompletedState(UserMenuStateBase):
    """
    Displays completion message after successful video repurposing.

    Shows success confirmation with options to process another video
    or return to the main menu.
    """

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True, as the repurpose video completed state waits for user input.
        """
        return True

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the repurpose video completed state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        return RepurposeVideoCompletedConst.NEXT_STATES_MAP.get(input_data, self._DefaultState())

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the completion message to the user.

        Args:
            chat: The chat to display the message in.
            user: The user viewing the message.
        """
        is_err = self._GetParamOrDefault(user, UserMenuParams.CONFIG_FILTER_SEND_ERR, False)
        buttons = []
        if not is_err:
            buttons.append([self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.REPURPOSE_VIDEO)])
        buttons.append([self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.START_MENU)])

        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_AND_DELETE,
            chat,
            user,
            self.translator.GetSentence("REPURPOSE_VIDEO_COMPLETED_MSG" if not is_err else "REPURPOSE_VIDEO_SEND_ERROR"),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
