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
from telegram_video_repurpose_bot.config.loader.config_section_loader import ConfigSectionLoader


class ConfigSectionsLoader:
    """Class for loading multiple configuration sections."""

    config_section_loader: ConfigSectionLoader

    def __init__(self,
                 config_parser: configparser.ConfigParser) -> None:
        """
        Construct class.

        Args:
            config_parser: Configuration parser
        """
        self.config_section_loader = ConfigSectionLoader(config_parser)

    def LoadSections(self,
                     sections: ConfigSectionsType) -> ConfigObject:
        """
        Load configuration sections.

        Args:
            sections: Configuration sections

        Returns:
            ConfigObject: Loaded configuration object
        """
        config_obj = ConfigObject()
        for section_name, section in sections.items():
            self.config_section_loader.LoadSection(config_obj, section_name, section)

        return config_obj
