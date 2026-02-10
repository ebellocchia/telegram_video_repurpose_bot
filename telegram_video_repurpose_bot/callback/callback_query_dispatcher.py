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

from typing import Any

import pyrogram

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.misc.helpers import ChatHelper, UserHelper
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


class CallbackQueryTypes:
    """Class containing callback query type constants."""

    BACK: str = "back_cbk"
    START_MENU: str = "start_menu_cbk"
    CONFIG_MAIN_MENU: str = "config_main_menu_cbk"
    CONFIG_BOT_ACCESS: str = "config_bot_access_cbk"
    CONFIG_BOT_ACCESS_ADD: str = "config_bot_access_add_cbk"
    CONFIG_BOT_ACCESS_REMOVE: str = "config_bot_access_remove_cbk"
    CONFIG_BOT_ACCESS_SHOW: str = "config_bot_access_show_cbk"
    CONFIG_AUDIO_PARAMS: str = "config_audio_params_cbk"
    CONFIG_VIDEO_PARAMS: str = "config_video_params_cbk"
    CONFIG_FILTER_TOGGLE: str = "config_filter_toggle_cbk"
    CONFIG_FILTER_DISABLE: str = "config_filter_disable_cbk"
    CONFIG_FILTER_ENABLE: str = "config_filter_enable_cbk"
    CONFIG_FILTER_SET_VALUE: str = "config_filter_set_value_cbk"
    CONFIG_MANAGE_PARAMS: str = "config_manage_params_cbk"
    CONFIG_LOAD_PARAMS: str = "config_load_params_cbk"
    CONFIG_SAVE_PARAMS: str = "config_save_params_cbk"
    CONFIG_SHOW_PARAMS: str = "config_show_params_cbk"
    CONFIG_FILTERS_DOC: str = "config_filters_doc_cbk"
    INFO_BOT: str = "info_bot_cbk"
    REPURPOSE_VIDEO: str = "repurpose_video_cbk"


class CallbackQueryDispatcher:
    """Class for dispatching callback queries to appropriate handlers."""

    config: ConfigObject
    logger: Logger
    translator: TranslationLoader

    def __init__(self,
                 config: ConfigObject,
                 logger: Logger,
                 translator: TranslationLoader) -> None:
        """
        Construct class.

        Args:
            config: Configuration object
            logger: Logger instance
            translator: Translation loader
        """
        self.config = config
        self.logger = logger
        self.translator = translator

    async def Dispatch(self,
                       client: pyrogram.Client,
                       cbk_query: pyrogram.types.CallbackQuery,
                       **kwargs: Any) -> None:
        """
        Dispatch a callback query to the appropriate handler.

        Args:
            client: Pyrogram client
            cbk_query: Callback query object
            **kwargs: Additional keyword arguments
        """
        if cbk_query.message is None or cbk_query.message.chat is None:
            self.logger.GetLogger().warning(f"Invalid callback received:\n{cbk_query}")
            return

        chat = cbk_query.message.chat
        user = cbk_query.from_user

        if not ChatHelper.IsPrivateChat(chat, user):
            return

        self.logger.GetLogger().info(
            f"Dispatching callback {cbk_query.data} from {UserHelper.GetNameOrId(user)}"    # type: ignore
        )

        await kwargs["user_menu"].OnCallback(chat, user, cbk_query.data)
