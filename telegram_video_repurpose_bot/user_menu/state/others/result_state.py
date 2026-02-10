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

from typing import Any, Dict

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


class ResultState(UserMenuStateBase):
    """
    Displays operation results with navigation options.

    Shows result messages (success, error, info) with buttons to return
    to previous state or go back to start menu.
    """

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True, as the result state waits for user input.
        """
        return True

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the result state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.START_MENU:
            return UserMenuStateTypes.START_MENU
        if input_data == CallbackQueryTypes.BACK:
            sentence_args = self._GetParam(user, UserMenuParams.SENTENCE_ARGS)
            if "back_state" in sentence_args:
                return sentence_args["back_state"]
        return self._DefaultState()

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the result message to the user.

        Args:
            chat: The chat to display the result in.
            user: The user viewing the result.
        """
        # Get parameters
        sentence_args = self._GetParam(user, UserMenuParams.SENTENCE_ARGS)

        # Send message
        await self.message_sender.SendMessage(
            sentence_args.get("msg_type", MenuMessageSenderTypes.SEND_OR_EDIT),
            chat,
            user,
            self.translator.GetSentence(
                self._GetParam(user, UserMenuParams.SENTENCE_ID),
                **sentence_args
            ),
            reply_markup=self.__BuildButtons(sentence_args)
        )

    def __BuildButtons(self,
                       sentence_args: Dict[str, Any]) -> InlineKeyboardMarkup:
        """
        Build navigation buttons for the result message.

        Args:
            sentence_args: Dictionary containing sentence arguments and button configuration.

        Returns:
            An InlineKeyboardMarkup with appropriate buttons.
        """
        btns = []
        if "back_state" in sentence_args:
            btns.append([self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.BACK)])
        else:
            btns.append([self.menu_btn_builder.KeyboardButtonCbk(UserMenuBtnTypes.START_MENU)])

        return InlineKeyboardMarkup(btns)
