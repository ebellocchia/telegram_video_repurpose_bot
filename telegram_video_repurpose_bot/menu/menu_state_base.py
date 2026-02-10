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

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pyrogram

from telegram_video_repurpose_bot.bot.bot_config_manager import BotConfigManager
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSender
from telegram_video_repurpose_bot.menu.menu_state_params import MenuStateParam, MenuStateParams
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader


@dataclass
class MenuStateBaseInitParams:
    """Parameters for MenuStateBase initialization."""
    client: pyrogram.Client
    bot_config_mgr: BotConfigManager
    logger: Logger
    message_sender: MenuMessageSender
    state_params: MenuStateParams
    translator: TranslationLoader


class MenuStateBase(ABC):
    """
    Abstract base class for menu states in a state machine.

    Defines the contract for menu states including execution logic, display,
    input waiting behavior, and parameter management. Subclasses implement
    specific state behaviors and transitions.
    """
    client: pyrogram.Client
    bot_config_mgr: BotConfigManager
    bot_config: ConfigObject
    logger: Logger
    message_sender: MenuMessageSender
    state_params: MenuStateParams
    translator: TranslationLoader

    def __init__(self,
                 params: MenuStateBaseInitParams) -> None:
        """
        Initialize the menu state base.

        Args:
            params: MenuStateBaseInitParams containing initialization parameters.
        """
        self.client = params.client
        self.bot_config_mgr = params.bot_config_mgr
        self.bot_config = params.bot_config_mgr.GetConfig()
        self.logger = params.logger
        self.message_sender = params.message_sender
        self.state_params = params.state_params
        self.translator = params.translator

    @abstractmethod
    async def Execute(self,
                      user: pyrogram.types.User,
                      input_data: str) -> MenuStateTypes:
        """
        Execute the state logic.

        Args:
            user: The user executing the state.
            input_data: Input data from user interaction.

        Returns:
            The next menu state type to transition to.
        """

    @abstractmethod
    async def Show(self,
                   chat: pyrogram.types.Chat,
                   user: pyrogram.types.User) -> None:
        """
        Display the state content to the user.

        Args:
            chat: The chat to display content in.
            user: The user viewing the state.
        """

    @staticmethod
    @abstractmethod
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True if the state waits for input, False otherwise.
        """

    @abstractmethod
    def StateParams(self,
                    user: pyrogram.types.User) -> MenuStateParam:
        """
        Get the state parameters for a user.

        Args:
            user: The user to get parameters for.

        Returns:
            The MenuStateParam object for the user.
        """

    def _StateName(self) -> str:
        """
        Get the state class name.

        Returns:
            The class name of the state.
        """
        return self.__class__.__name__
