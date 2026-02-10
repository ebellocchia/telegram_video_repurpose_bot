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

from telegram_video_repurpose_bot.bot.bot_config import BotConfig
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.config.loader.config_sections_file_loader import ConfigSectionsFileLoader
from telegram_video_repurpose_bot.config.saver.config_sections_file_saver import ConfigSectionsFileSaver
from telegram_video_repurpose_bot.logger.logger import Logger


class BotConfigManager:
    """Manager for bot configuration."""

    bot_config: ConfigObject
    config_file_name: str

    def __init__(self,
                 config_file_name: str) -> None:
        """
        Initialize bot configuration manager.

        Args:
            config_file_name: Configuration file name.
        """
        self.config_file_name = config_file_name
        self.LoadConfig()

    def GetConfig(self) -> ConfigObject:
        """
        Gets the bot configuration.

        Returns:
            The bot configuration object.
        """
        return self.bot_config

    def LoadConfig(self) -> None:
        """Load the FFMPEG configuration from file."""
        self.bot_config = ConfigSectionsFileLoader.Load(self.config_file_name, BotConfig)

    def SaveConfig(self,
                   logger: Logger) -> None:
        """
        Save the current FFMPEG configuration to file.

        Args:
            logger: The logger instance.
        """
        ConfigSectionsFileSaver(logger).Save(
            self.config_file_name,
            self.bot_config,
            BotConfig
        )
