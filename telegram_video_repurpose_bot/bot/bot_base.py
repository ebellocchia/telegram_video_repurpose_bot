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
from pyrogram import Client, idle

from telegram_video_repurpose_bot.bot.bot_config_manager import BotConfigManager
from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.bot.bot_handlers_config import BotHandlersConfig
from telegram_video_repurpose_bot.bot.bot_handlers_config_typing import BotHandlersConfigType
from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryDispatcher
from telegram_video_repurpose_bot.command.command_dispatcher import CommandDispatcher, CommandTypes
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.message.message_dispatcher import MessageDispatcher, MessageTypes
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


class BotBase:
    """Base class for the Telegram bot."""

    config_mgr: BotConfigManager
    cbk_query_dispatcher: CallbackQueryDispatcher
    client: pyrogram.Client
    cmd_dispatcher: CommandDispatcher
    config: ConfigObject
    config_file_name: str
    logger: Logger
    msg_dispatcher: MessageDispatcher
    translator: TranslationLoader

    def __init__(self,
                 config_file_name: str) -> None:
        """
        Construct class.

        Args:
            config_file_name: Configuration file name
        """
        self.config_file_name = config_file_name
        self.__InitializeBot(config_file_name)
        self.__InitializeClient()
        self.logger.GetLogger().info("Bot initialization completed")

    async def Run(self) -> None:
        """Run the bot asynchronously."""
        self.logger.GetLogger().info("Bot started!\n")
        async with self.client:
            await idle()

    def __SetupHandlers(self,
                        handlers_config: BotHandlersConfigType) -> None:
        """
        Set up message handlers for the bot.

        Args:
            handlers_config: Handlers configuration
        """
        def create_handler(handler_type, handler_cfg):
            async def async_callback(client, message):
                return await handler_cfg["callback"](self, client, message)
            return handler_type(async_callback, handler_cfg["filters"])

        for curr_hnd_type, curr_hnd_cfg in handlers_config.items():
            for handler_cfg in curr_hnd_cfg:
                self.client.add_handler(
                    create_handler(curr_hnd_type, handler_cfg)
                )
        self.logger.GetLogger().info("Bot handlers set")

    async def DispatchCommand(self,
                              client: pyrogram.Client,
                              message: pyrogram.types.Message,
                              cmd_type: CommandTypes,
                              **kwargs: Any) -> None:
        """
        Dispatch a command to the command dispatcher.

        Args:
            client: Pyrogram client
            message: Message object
            cmd_type: Command type
            **kwargs: Additional keyword arguments
        """
        await self.cmd_dispatcher.Dispatch(client, message, cmd_type, **kwargs)

    async def DispatchCallbackQuery(self,
                                    client: pyrogram.Client,
                                    cbk_query: pyrogram.types.CallbackQuery,
                                    **kwargs: Any) -> None:
        """
        Dispatch a callback query to the callback query dispatcher.

        Args:
            client: Pyrogram client
            cbk_query: Callback query object
            **kwargs: Additional keyword arguments
        """
        await self.cbk_query_dispatcher.Dispatch(client, cbk_query, **kwargs)

    async def HandleMessage(self,
                            client: pyrogram.Client,
                            message: pyrogram.types.Message,
                            msg_type: MessageTypes,
                            **kwargs: Any) -> None:
        """
        Handle a message by dispatching it to the message dispatcher.

        Args:
            client: Pyrogram client
            message: Message object
            msg_type: Message type
            **kwargs: Additional keyword arguments
        """
        await self.msg_dispatcher.Dispatch(client, message, msg_type, **kwargs)

    def __InitializeBot(self,
                        config_file_name: str) -> None:
        """
        Initialize the bot components.

        Args:
            config_file_name: Configuration file name
        """
        self.config_mgr = BotConfigManager(config_file_name)
        self.config = self.config_mgr.GetConfig()
        self.logger = Logger(self.config)
        self.translator = TranslationLoader(self.logger)
        self.translator.Load(self.config.GetValue(BotConfigTypes.APP_LANG_FILE))
        self.cmd_dispatcher = CommandDispatcher(
            self.config,
            self.logger,
            self.translator
        )
        self.cbk_query_dispatcher = CallbackQueryDispatcher(
            self.config,
            self.logger,
            self.translator
        )
        self.msg_dispatcher = MessageDispatcher(
            self.config,
            self.logger,
            self.translator
        )

    def __InitializeClient(self) -> None:
        """Initialize the Pyrogram client."""
        self.client = Client(
            self.config.GetValue(BotConfigTypes.SESSION_NAME),
            api_id=self.config.GetValue(BotConfigTypes.API_ID),
            api_hash=self.config.GetValue(BotConfigTypes.API_HASH),
            bot_token=self.config.GetValue(BotConfigTypes.BOT_TOKEN)
        )
        self.__SetupHandlers(BotHandlersConfig)
