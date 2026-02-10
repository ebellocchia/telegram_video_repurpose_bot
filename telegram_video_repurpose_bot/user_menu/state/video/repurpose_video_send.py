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
from pyrogram.errors import RPCError
from typing_extensions import override

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


class RepurposeVideoSendState(UserMenuStateBase):
    """
    Sends processed video to user with processing parameters.

    Transmits the repurposed video file to the user with caption containing
    processing time and applied parameters. Cleans up temporary files if configured.
    """

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            False, as this is a non-interactive state that doesn't wait for input.
        """
        return False

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the repurpose video send state logic.

        Args:
            user: The user executing the state.
            input_data: Input data from user interaction.

        Returns:
            The next menu state type (repurpose video completed state).
        """
        if input_data == CallbackQueryTypes.START_MENU:
            return UserMenuStateTypes.START_MENU
        return UserMenuStateTypes.REPURPOSE_VIDEO_COMPLETED

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Send the processed video to the user with parameters.

        Args:
            chat: The chat to send the video to.
            user: The user receiving the video.
        """
        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("REPURPOSE_VIDEO_SENDING_MSG")
        )
        # Get video params
        video_orig_file_name = self._GetParam(user, UserMenuParams.VIDEO_ORIG_FILE_NAME)
        video_proc_file_name = self._GetParam(user, UserMenuParams.VIDEO_PROC_FILE_NAME)
        video_proc_elapsed_time = self._GetParam(user, UserMenuParams.VIDEO_PROC_ELAPSED_TIME)
        video_proc_params = self._GetParam(user, UserMenuParams.VIDEO_PROC_PARAMS)
        self.logger.GetLogger().info(f"Sending video {video_proc_file_name}...")
        # Send video
        try:
            await self.message_sender.SendVideo(
                MenuMessageSenderTypes.SEND,
                chat,
                user,
                video_proc_file_name,
                caption=self.translator.GetSentence("REPURPOSE_VIDEO_PARAMS_MSG",
                                                    video_elapsed_time=round(video_proc_elapsed_time, 2),
                                                    video_params=str(video_proc_params))
            )
        except (ValueError, RPCError):
            self._SetParams(user, config_filter_send_err=True)
        finally:
            self.__RemoveVideoFile(video_orig_file_name, BotConfigTypes.VIDEO_DOWNLOAD_DELETE_FILE)
            self.__RemoveVideoFile(video_proc_file_name, BotConfigTypes.VIDEO_PROCESS_DELETE_FILE)

    def __RemoveVideoFile(self,
                          file_name: str,
                          config_type: BotConfigTypes) -> None:
        """
        Remove video file if configured to do so.

        Args:
            file_name: The path to the video file to remove.
            config_type: The configuration type to check for deletion permission.
        """
        if not self.bot_config.GetValue(config_type):
            return

        try:
            os.remove(file_name)
            self.logger.GetLogger().info(f"Removed video file {file_name}...")
        except OSError:
            self.logger.GetLogger().warning(f"Unable to remove video file {file_name}")
