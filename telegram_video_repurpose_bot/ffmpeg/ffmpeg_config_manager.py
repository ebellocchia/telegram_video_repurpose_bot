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

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.config.loader.config_sections_file_loader import ConfigSectionsFileLoader
from telegram_video_repurpose_bot.config.saver.config_sections_file_saver import ConfigSectionsFileSaver
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config import FfmpegConfig
from telegram_video_repurpose_bot.logger.logger import Logger


class FfmpegConfigManager:
    """Manager for FFmpeg configuration."""

    bot_config: ConfigObject
    logger: Logger
    ffmpeg_config: ConfigObject

    def __init__(self,
                 bot_config: ConfigObject,
                 logger: Logger) -> None:
        """
        Initialize FFmpeg configuration manager.

        Args:
            bot_config: Bot configuration object.
            logger: The logger instance.
        """
        self.bot_config = bot_config
        self.logger = logger
        self.LoadConfig()

    def GetConfig(self) -> ConfigObject:
        """
        Gets the FFmpeg configuration.

        Returns:
            The FFmpeg configuration object.
        """
        return self.ffmpeg_config

    def LoadConfig(self) -> None:
        """Load the FFMPEG configuration from file."""
        self.ffmpeg_config = ConfigSectionsFileLoader.Load(
            self.bot_config.GetValue(BotConfigTypes.VIDEO_FFMPEG_PARAMS_FILE),
            FfmpegConfig
        )

    def SaveConfig(self) -> None:
        """Save the current FFMPEG configuration to file."""
        ConfigSectionsFileSaver(self.logger).Save(
            self.bot_config.GetValue(BotConfigTypes.VIDEO_FFMPEG_PARAMS_FILE),
            self.ffmpeg_config,
            FfmpegConfig
        )
