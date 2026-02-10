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

import asyncio
import time

import pyrogram
from typing_extensions import override

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_manager import FfmpegConfigManager
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase, UserMenuStateBaseInitParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes
from telegram_video_repurpose_bot.video.video_processor import VideoProcessor
from telegram_video_repurpose_bot.video.video_processor_ex import VideoProcessError


class RepurposeVideoProcessState(UserMenuStateBase):
    """
    Executes video processing with filters and encoding.

    Applies video processor to transform the uploaded video, tracking
    processing time and parameters. Transitions to send state on success.
    """

    ffmpeg_config_mgr: FfmpegConfigManager
    ffmpeg_semaphore: asyncio.Semaphore

    def __init__(self,
                 params: UserMenuStateBaseInitParams) -> None:
        """
        Initialize the repurpose video process state.

        Args:
            params: UserMenuStateBaseInitParams containing initialization parameters.
        """
        super().__init__(params)
        self.ffmpeg_config_mgr = params.ffmpeg_config_mgr
        self.ffmpeg_semaphore = asyncio.Semaphore(self.bot_config.GetValue(BotConfigTypes.VIDEO_MAX_PROCESSES))

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
        Execute the video processing logic.

        Args:
            user: The user executing the state.
            input_data: Input data from user interaction.

        Returns:
            The next menu state type (repurpose video send state on success).
        """
        try:
            start_time = time.time()
            video_proc = VideoProcessor(
                self.bot_config,
                self.ffmpeg_config_mgr.GetConfig(),
                self.ffmpeg_semaphore,
                self.logger
            )
            video_proc_file_name, video_proc_params = await video_proc.ProcessVideo(
                self._GetParam(user, UserMenuParams.VIDEO_ORIG_FILE_NAME)
            )
            end_time = time.time()

            self._AddParams(user, video_proc_elapsed_time=end_time - start_time)
            self._AddParams(user, video_proc_file_name=video_proc_file_name)
            self._AddParams(user, video_proc_params=video_proc_params)
            return UserMenuStateTypes.REPURPOSE_VIDEO_SEND
        except VideoProcessError:
            self.logger.GetLogger().exception("Unable to process video")
            return self._ResultState(user, "REPURPOSE_VIDEO_PROCESS_ERROR")

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the processing status message to the user.

        Args:
            chat: The chat to display the message in.
            user: The user viewing the message.
        """
        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("REPURPOSE_VIDEO_PROCESSING_MSG")
        )
