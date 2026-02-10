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
from enum import Enum

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.config.config_typing import ConfigSectionType
from telegram_video_repurpose_bot.logger.logger import Logger


class ConfigSectionSaver:
    """Class for saving a configuration section."""

    config_parser: configparser.ConfigParser
    logger: Logger

    def __init__(self,
                 config_parser: configparser.ConfigParser,
                 logger: Logger) -> None:
        """
        Construct class.

        Args:
            config_parser: Configuration parser
            logger: Logger instance
        """
        self.config_parser = config_parser
        self.logger = logger

    def SaveSection(self,
                    config_obj: ConfigObject,
                    section_name: str,
                    section: ConfigSectionType) -> None:
        """
        Save a configuration section.

        Args:
            config_obj: Configuration object
            section_name: Section name
            section: Section configuration
        """
        self.logger.GetLogger().info(f"Section [{section_name}]")

        self.config_parser[section_name] = {}
        for field in section:
            try:
                field_val = config_obj.GetValue(field["type"])

                if "def_val" in field and field_val == field["def_val"] and not isinstance(field_val, (list, set)):
                    continue

                if isinstance(field_val, Enum):
                    field_val = field_val.name.upper()
                elif isinstance(field_val, (list, set)):
                    field_val = ",".join(map(str, field_val))
                else:
                    field_val = str(field_val)
                self.config_parser[section_name][field["name"]] = field_val
                self.logger.GetLogger().info(f"  {field['name']}: {field_val}")

            except KeyError:
                continue
