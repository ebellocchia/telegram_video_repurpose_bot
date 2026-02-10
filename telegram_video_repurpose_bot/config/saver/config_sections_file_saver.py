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

import configparser

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.config.config_typing import ConfigSectionsType
from telegram_video_repurpose_bot.config.saver.config_sections_saver import ConfigSectionsSaver
from telegram_video_repurpose_bot.logger.logger import Logger


class ConfigSectionsFileSaver:
    """Class for saving configuration sections to a file."""

    logger: Logger

    def __init__(self,
                 logger: Logger) -> None:
        """
        Construct class.

        Args:
            logger: Logger instance
        """
        self.logger = logger

    def Save(self,
             file_name: str,
             config_obj: ConfigObject,
             sections: ConfigSectionsType) -> None:
        """
        Save configuration to file.

        Args:
            file_name: Configuration file name
            config_obj: Configuration object
            sections: Configuration sections
        """
        self.logger.GetLogger().info(f"Savings configuration file {file_name}...")

        config_parser = configparser.ConfigParser()
        ConfigSectionsSaver(config_parser, self.logger).SaveSections(config_obj, sections)

        with open(file_name, "w", encoding="utf-8") as fout:
            config_parser.write(fout)
