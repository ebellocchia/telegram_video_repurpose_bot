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

import os

import pyrogram
from typing_extensions import override

from telegram_video_repurpose_bot.app.app_users import AppUsers
from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class RepurposeVideoStartState(UserMenuStateBase):
    """
    Initiates video repurposing by prompting for video upload.

    Displays message requesting video input from user,
    waits for video file submission before processing.
    """

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True, as the repurpose video start state waits for user input.
        """
        return True

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the repurpose video start state logic.

        Args:
            user: The user executing the state.
            input_data: The video file path from user submission.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.BACK:
            return UserMenuStateTypes.START_MENU

        # input_data contains the file path
        if os.path.isfile(input_data):
            self._AddParams(user, video_orig_file_name=input_data)
            return UserMenuStateTypes.REPURPOSE_VIDEO_PROCESS
        return UserMenuStateTypes.START_MENU

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the video input prompt to the user.

        Args:
            chat: The chat to display the prompt in.
            user: The user viewing the prompt.
        """
        if not AppUsers(self.bot_config).IsAuthorized(user):
            msg = self.translator.GetSentence("USER_AUTH_BOT_ERR_MSG")
        else:
            msg = self.translator.GetSentence("REPURPOSE_VIDEO_START_MSG")

        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            msg,
            reply_markup=self.menu_btn_builder.KeyboardMarkupCbk(UserMenuBtnTypes.BACK)
        )
