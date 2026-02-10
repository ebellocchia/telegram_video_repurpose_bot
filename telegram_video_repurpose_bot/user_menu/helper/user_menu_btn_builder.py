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

from enum import auto, unique

from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.menu.menu_btn import MenuBtn
from telegram_video_repurpose_bot.menu.menu_btn_builder import MenuBtnBuilder, MenuBtnDataType, MenuBtnTypes
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


@unique
class UserMenuBtnTypes(MenuBtnTypes):
    """User menu button types."""
    BACK = auto()
    CONFIG_MAIN_MENU = auto()
    CONFIG_BOT_ACCESS = auto()
    CONFIG_BOT_ACCESS_ADD = auto()
    CONFIG_BOT_ACCESS_REMOVE = auto()
    CONFIG_BOT_ACCESS_SHOW = auto()
    CONFIG_AUDIO_PARAMS = auto()
    CONFIG_VIDEO_PARAMS = auto()
    CONFIG_FILTER_TOGGLE = auto()
    CONFIG_FILTER_ENABLE = auto()
    CONFIG_FILTER_DISABLE = auto()
    CONFIG_FILTER_SET_VALUE = auto()
    CONFIG_SHOW_PARAMS = auto()
    CONFIG_MANAGE_PARAMS = auto()
    CONFIG_LOAD_PARAMS = auto()
    CONFIG_SAVE_PARAMS = auto()
    CONFIG_FILTERS_DOC = auto()
    INFO_BOT = auto()
    REPURPOSE_VIDEO = auto()
    START_MENU = auto()


class UserMenuBtnConst:
    """Constants for user menu buttons class."""
    BTN_DATA: MenuBtnDataType = {
        UserMenuBtnTypes.CONFIG_MAIN_MENU: MenuBtn(
            "CONFIG_MAIN_MENU_BTN",
            CallbackQueryTypes.CONFIG_MAIN_MENU
        ),
        UserMenuBtnTypes.CONFIG_BOT_ACCESS: MenuBtn(
            "CONFIG_BOT_ACCESS_BTN",
            CallbackQueryTypes.CONFIG_BOT_ACCESS
        ),
        UserMenuBtnTypes.CONFIG_BOT_ACCESS_ADD: MenuBtn(
            "CONFIG_BOT_ACCESS_ADD_BTN",
            CallbackQueryTypes.CONFIG_BOT_ACCESS_ADD
        ),
        UserMenuBtnTypes.CONFIG_BOT_ACCESS_REMOVE: MenuBtn(
            "CONFIG_BOT_ACCESS_REMOVE_BTN",
            CallbackQueryTypes.CONFIG_BOT_ACCESS_REMOVE
        ),
        UserMenuBtnTypes.CONFIG_BOT_ACCESS_SHOW: MenuBtn(
            "CONFIG_BOT_ACCESS_SHOW_BTN",
            CallbackQueryTypes.CONFIG_BOT_ACCESS_SHOW
        ),
        UserMenuBtnTypes.CONFIG_AUDIO_PARAMS: MenuBtn(
            "CONFIG_AUDIO_PARAMS_BTN",
            CallbackQueryTypes.CONFIG_AUDIO_PARAMS
        ),
        UserMenuBtnTypes.CONFIG_VIDEO_PARAMS: MenuBtn(
            "CONFIG_VIDEO_PARAMS_BTN",
            CallbackQueryTypes.CONFIG_VIDEO_PARAMS
        ),
        UserMenuBtnTypes.CONFIG_FILTER_TOGGLE: MenuBtn(
            "CONFIG_FILTER_TOGGLE_BTN",
            CallbackQueryTypes.CONFIG_FILTER_TOGGLE
        ),
        UserMenuBtnTypes.CONFIG_FILTER_ENABLE: MenuBtn(
            "CONFIG_FILTER_ENABLE_BTN",
            CallbackQueryTypes.CONFIG_FILTER_ENABLE
        ),
        UserMenuBtnTypes.CONFIG_FILTER_DISABLE: MenuBtn(
            "CONFIG_FILTER_DISABLE_BTN",
            CallbackQueryTypes.CONFIG_FILTER_DISABLE
        ),
        UserMenuBtnTypes.CONFIG_FILTER_SET_VALUE: MenuBtn(
            "CONFIG_FILTER_SET_VALUE_BTN",
            CallbackQueryTypes.CONFIG_FILTER_SET_VALUE
        ),
        UserMenuBtnTypes.CONFIG_MANAGE_PARAMS: MenuBtn(
            "CONFIG_MANAGE_PARAMS_BTN",
            CallbackQueryTypes.CONFIG_MANAGE_PARAMS
        ),
        UserMenuBtnTypes.CONFIG_LOAD_PARAMS: MenuBtn(
            "CONFIG_LOAD_PARAMS_BTN",
            CallbackQueryTypes.CONFIG_LOAD_PARAMS
        ),
        UserMenuBtnTypes.CONFIG_SAVE_PARAMS: MenuBtn(
            "CONFIG_SAVE_PARAMS_BTN",
            CallbackQueryTypes.CONFIG_SAVE_PARAMS
        ),
        UserMenuBtnTypes.CONFIG_SHOW_PARAMS: MenuBtn(
            "CONFIG_SHOW_PARAMS_BTN",
            CallbackQueryTypes.CONFIG_SHOW_PARAMS
        ),
        UserMenuBtnTypes.CONFIG_FILTERS_DOC: MenuBtn(
            "CONFIG_FILTERS_DOC_BTN",
            CallbackQueryTypes.CONFIG_FILTERS_DOC
        ),
        UserMenuBtnTypes.BACK: MenuBtn("BACK_BTN", CallbackQueryTypes.BACK),
        UserMenuBtnTypes.INFO_BOT: MenuBtn("INFO_BOT_BTN", CallbackQueryTypes.INFO_BOT),
        UserMenuBtnTypes.REPURPOSE_VIDEO: MenuBtn("REPURPOSE_VIDEO_BTN", CallbackQueryTypes.REPURPOSE_VIDEO),
        UserMenuBtnTypes.START_MENU: MenuBtn("START_MENU_BTN", CallbackQueryTypes.START_MENU),
    }


class UserMenuBtnBuilder(MenuBtnBuilder):
    """
    Builds user menu buttons with translated labels.

    Creates inline keyboard buttons specific to user menu interactions
    with translated button text for video processing and navigation.
    """

    def __init__(self,
                 translator: TranslationLoader) -> None:
        """
        Initialize the user menu button builder.

        Args:
            translator: The translation loader instance.
        """
        super().__init__(UserMenuBtnConst.BTN_DATA, translator)
