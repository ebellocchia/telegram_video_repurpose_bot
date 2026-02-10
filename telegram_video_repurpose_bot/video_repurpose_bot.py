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

from telegram_video_repurpose_bot.bot.bot_base import BotBase
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.user_menu.user_menu import UserMenu


class VideoRepurposeBot(BotBase):
    """
    Main bot implementation for video repurposing with Telegram integration.

    Extends the base bot with video processing capabilities, manages FFmpeg
    configuration, and orchestrates the user menu for interactive video editing.
    """

    ffmpeg_config: ConfigObject

    def __init__(self,
                 config_file: str) -> None:
        """
        Initialize the video repurpose bot.

        Args:
            config_file: Path to the configuration file.
        """
        super().__init__(config_file)
        self.user_menu = UserMenu(
            self.client,
            self.config_mgr,
            self.logger,
            self.translator
        )
