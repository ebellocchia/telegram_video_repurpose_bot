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

from enum import Enum
from typing import Dict

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_video_repurpose_bot.menu.menu_btn import MenuBtn
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


class MenuBtnTypes(Enum):
    """Menu button types."""


MenuBtnDataType = Dict[MenuBtnTypes, MenuBtn]


class MenuBtnBuilder:
    """
    Builds inline keyboard buttons and markups with translated labels.

    Creates Telegram inline keyboard buttons and markups with callback or URL
    actions, translating button labels from a translation loader.
    """

    translator: TranslationLoader

    def __init__(self,
                 btn_data: MenuBtnDataType,
                 translator: TranslationLoader) -> None:
        """
        Initialize the menu button builder.

        Args:
            btn_data: Dictionary mapping button types to MenuBtn objects.
            translator: The translation loader for button labels.
        """
        self.btn_data = btn_data
        self.translator = translator

    @staticmethod
    def KeyboardGenericButtonCbk(btn_id: str) -> InlineKeyboardButton:
        """
        Create an inline keyboard button with callback data.

        Args:
            btn_id: The ID of button to create.

        Returns:
            An InlineKeyboardButton with callback data.
        """
        return InlineKeyboardButton(btn_id,
                                    callback_data=btn_id)

    def KeyboardButtonCbk(self,
                          btn_type: MenuBtnTypes) -> InlineKeyboardButton:
        """
        Create an inline keyboard button with callback data.

        Args:
            btn_type: The type of button to create.

        Returns:
            An InlineKeyboardButton with callback data.
        """
        btn = self.btn_data[btn_type]
        return InlineKeyboardButton(self.translator.GetSentence(btn.Id()),
                                    callback_data=btn.Callback())

    def KeyboardButtonUrl(self,
                          btn_type: MenuBtnTypes,
                          url: str) -> InlineKeyboardButton:
        """
        Create an inline keyboard button with URL.

        Args:
            btn_type: The type of button to create.
            url: The URL to open when the button is clicked.

        Returns:
            An InlineKeyboardButton with URL.
        """
        btn = self.btn_data[btn_type]
        return InlineKeyboardButton(self.translator.GetSentence(btn.Id()),
                                    url=url)

    def KeyboardMarkupCbk(self,
                          btn_type: MenuBtnTypes) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup with a single callback button.

        Args:
            btn_type: The type of button to include.

        Returns:
            An InlineKeyboardMarkup containing the callback button.
        """
        return InlineKeyboardMarkup(
            [
                [
                    self.KeyboardButtonCbk(btn_type)
                ]
            ]
        )

    def KeyboardMarkupUrl(self,
                          btn_type: MenuBtnTypes,
                          url: str) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard markup with a single URL button.

        Args:
            btn_type: The type of button to include.
            url: The URL to open when the button is clicked.

        Returns:
            An InlineKeyboardMarkup containing the URL button.
        """
        return InlineKeyboardMarkup(
            [
                [
                    self.KeyboardButtonUrl(btn_type, url)
                ]
            ]
        )
