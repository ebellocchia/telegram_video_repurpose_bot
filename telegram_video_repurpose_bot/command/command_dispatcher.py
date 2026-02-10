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

from typing import Any, Dict, Type

import pyrogram

from telegram_video_repurpose_bot.command.command_base import CommandBase
from telegram_video_repurpose_bot.command.command_types import CommandTypes
from telegram_video_repurpose_bot.command.commands import AliveCmd, HelpCmd
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


class CommandDispatcherConst:
    """Constants for command dispatcher class."""

    CMD_TYPE_TO_CLASS: Dict[CommandTypes, Type[CommandBase]] = {
        CommandTypes.ALIVE_CMD: AliveCmd,
        CommandTypes.HELP_CMD: HelpCmd,
    }


class CommandDispatcher:
    """Class for dispatching commands to appropriate handlers."""

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
                       message: pyrogram.types.Message,
                       cmd_type: CommandTypes,
                       **kwargs: Any) -> None:
        """
        Dispatch command to appropriate handler.

        Args:
            client: Pyrogram client
            message: Pyrogram message object
            cmd_type: Command type
            **kwargs: Additional keyword arguments
        """
        if not isinstance(cmd_type, CommandTypes):
            raise TypeError("Command type is not an enumerative of CommandTypes")

        self.logger.GetLogger().info(f"Dispatching command type: {cmd_type}")

        if cmd_type in CommandDispatcherConst.CMD_TYPE_TO_CLASS:
            cmd_class = CommandDispatcherConst.CMD_TYPE_TO_CLASS[cmd_type](client,
                                                                           self.config,
                                                                           self.logger,
                                                                           self.translator)
            await cmd_class.Execute(message, **kwargs)
