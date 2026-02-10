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
from telegram_video_repurpose_bot.config.config_typing import ConfigFieldType, ConfigSectionType
from telegram_video_repurpose_bot.config.loader.config_loader_ex import ConfigFieldNotExistentError, ConfigFieldValueError


class ConfigSectionLoader:
    """Class for loading a configuration section."""

    config_parser: configparser.ConfigParser

    def __init__(self,
                 config_parser: configparser.ConfigParser) -> None:
        """
        Construct class.

        Args:
            config_parser: Configuration parser
        """
        self.config_parser = config_parser

    def LoadSection(self,
                    config_obj: ConfigObject,
                    section_name: str,
                    section: ConfigSectionType) -> None:
        """
        Load a configuration section.

        Args:
            config_obj: Configuration object
            section_name: Section name
            section: Section configuration
        """
        print(f"Section [{section_name}]")

        for field in section:
            if self.__FieldShallBeLoaded(config_obj, field):
                self.__SetFieldValue(config_obj, section_name, field)
                self.__PrintFieldValue(config_obj, field)
            elif "def_val" in field:
                config_obj.SetValue(field["type"], field["def_val"])

    @staticmethod
    def __FieldShallBeLoaded(config_obj: ConfigObject,
                             field: ConfigFieldType) -> bool:
        """
        Get if field shall be loaded.

        Args:
            config_obj: Configuration object
            field: Field configuration

        Returns:
            bool: True if field shall be loaded, False otherwise
        """
        return field["load_if"](config_obj) if "load_if" in field else True

    def __SetFieldValue(self,
                        config_obj: ConfigObject,
                        section: str,
                        field: ConfigFieldType) -> None:
        """
        Set field value.

        Args:
            config_obj: Configuration object
            section: Section name
            field: Field configuration
        """
        try:
            field_val = self.config_parser[section][field["name"]]
        except KeyError as ex:
            if "def_val" not in field:
                raise ConfigFieldNotExistentError(f"Configuration field \"{field['name']}\" not found") from ex
            field_val = field["def_val"]
        else:
            if "conv_fct" in field:
                field_val = field["conv_fct"](field_val)
            if "valid_if" in field and not field["valid_if"](config_obj, field_val):
                raise ConfigFieldValueError(f"Value \"{field_val}\" is not valid for field \"{field['name']}\"")

        config_obj.SetValue(field["type"], field_val)

    @staticmethod
    def __PrintFieldValue(config_obj: ConfigObject,
                          field: ConfigFieldType) -> None:
        """
        Print field value.

        Args:
            config_obj: Configuration object
            field: Field configuration
        """
        if "print_fct" in field:
            print(f"- {field['name']}: {field['print_fct'](config_obj.GetValue(field['type']))}")
        else:
            print(f"- {field['name']}: {config_obj.GetValue(field['type'])}")
