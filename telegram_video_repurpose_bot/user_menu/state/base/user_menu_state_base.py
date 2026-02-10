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

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import pyrogram
from typing_extensions import override

from telegram_video_repurpose_bot.bot.bot_config_manager import BotConfigManager
from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_manager import FfmpegConfigManager
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSender
from telegram_video_repurpose_bot.menu.menu_state_base import MenuStateBase, MenuStateBaseInitParams
from telegram_video_repurpose_bot.menu.menu_state_params import MenuStateParam, MenuStateParams
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.misc.helpers import UserHelper
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnBuilder
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes


@dataclass
class UserMenuStateBaseInitParams:
    """Parameters for UserMenuStateBase initialization."""
    client: pyrogram.Client
    bot_config_mgr: BotConfigManager
    ffmpeg_config_mgr: FfmpegConfigManager
    logger: Logger
    message_sender: MenuMessageSender
    state_params: MenuStateParams
    translator: TranslationLoader


class UserMenuStateBase(MenuStateBase):
    """
    Base class for all user menu states with error handling and validation.

    Extends MenuStateBase with user-specific functionality including parameter
    management, username validation, error handling, and result state transitions.
    """

    menu_btn_builder: UserMenuBtnBuilder

    def __init__(self,
                 params: UserMenuStateBaseInitParams) -> None:
        """
        Initialize the user menu state base.

        Args:
            params: UserMenuStateBaseInitParams containing initialization parameters.
        """
        super().__init__(
            MenuStateBaseInitParams(
                params.client,
                params.bot_config_mgr,
                params.logger,
                params.message_sender,
                params.state_params,
                params.translator
            )
        )
        self.menu_btn_builder = UserMenuBtnBuilder(params.translator)

    @override
    async def Execute(self,
                      user: pyrogram.types.User,
                      input_data: str) -> MenuStateTypes:
        """
        Execute the state with error handling and validation.

        Args:
            user: The user executing the state.
            input_data: Input data from user interaction.

        Returns:
            The next menu state type to transition to.
        """
        # Log
        self.logger.GetLogger().info(
            f"Executing state {self._StateName()} for user {UserHelper.GetNameOrId(user)}, "
            f"input data: {input_data}, state data -> {self.StateParams(user)}"
        )

        # Check if username is set
        if user.username is None:
            return self._ResultState(user, "NO_USERNAME_ERR_MSG")

        # Execute state
        try:
            next_state = await self._Execute(user, input_data)
        except Exception:
            # Log
            self.logger.GetLogger().exception(
                f"Exception raised during execution of user {UserHelper.GetNameOrId(user)}, input data: {input_data}, "
                f"state data -> {self.StateParams(user)}"
            )
            next_state = self._ResultState(user,
                                           "GENERIC_ERR_MSG",
                                           bot_support=self.bot_config.GetValue(BotConfigTypes.APP_SUPPORT))
        return next_state

    @override
    async def Show(self,
                   chat: pyrogram.types.Chat,
                   user: pyrogram.types.User) -> None:
        """
        Display the state content with error handling.

        Args:
            chat: The chat to display content in.
            user: The user viewing the state.
        """
        # Log
        self.logger.GetLogger().info(
            f"Showing state {self._StateName()} for user {UserHelper.GetNameOrId(user)}, "
            f"state data -> {self.StateParams(user)}"
        )

        # Show state
        try:
            await self._Show(chat, user)
        except Exception:
            # Log
            self.logger.GetLogger().exception(
                f"Exception raised during showing of user {UserHelper.GetNameOrId(user)}, "
                f"state data -> {self.StateParams(user)}"
            )

    @override
    def StateParams(self,
                    user: pyrogram.types.User) -> MenuStateParam:
        """
        Get the state parameters for a user.

        Args:
            user: The user to get parameters for.

        Returns:
            The MenuStateParam object for the user.
        """
        return self.state_params.GetByUser(user)

    @staticmethod
    def _DefaultState() -> MenuStateTypes:
        """
        Get the default menu state.

        Returns:
            The default MenuStateTypes value.
        """
        return UserMenuStateTypes.START_MENU

    def _ResultState(self,
                     user: pyrogram.types.User,
                     sentence_id: str,
                     **kwargs: Any) -> MenuStateTypes:
        """
        Transition to the result state with a message.

        Args:
            user: The user transitioning to result state.
            sentence_id: The ID of the sentence to display.
            **kwargs: Additional parameters to pass to the result state.

        Returns:
            The result state type.
        """
        # Log
        self.logger.GetLogger().info(
            f"User {UserHelper.GetNameOrId(user)} exiting with result {sentence_id} in state {self._StateName()}"
        )
        # Add parameters
        self._AddParams(user, sentence_id=sentence_id, sentence_args=kwargs)
        # Go to result state
        return UserMenuStateTypes.RESULT

    def _AddParams(self,
                   user: pyrogram.types.User,
                   **kwargs: Any) -> None:
        """
        Add parameters to the user's state.

        Args:
            user: The user to add parameters for.
            **kwargs: Key-value pairs to add as parameters.
        """
        self.StateParams(user).AddMultiple({
            UserMenuParams(key): value for key, value in kwargs.items()
        })

    def _ExistParam(self,
                    user: pyrogram.types.User,
                    param: UserMenuParams) -> bool:
        """
        Check if a parameter exists for a user.

        Args:
            user: The user to check.
            param: The parameter to check for.

        Returns:
            True if the parameter exists, False otherwise.
        """
        return param in self.StateParams(user)

    def _DeleteParam(self,
                     user: pyrogram.types.User,
                     param: UserMenuParams) -> None:
        """
        Delete a parameter from the user's state.

        Args:
            user: The user to delete the parameter from.
            param: The parameter to delete.
        """
        self.StateParams(user).RemoveSingle(param)

    def _GetParam(self,
                  user: pyrogram.types.User,
                  param: UserMenuParams) -> Any:
        """
        Get a parameter value for a user.

        Args:
            user: The user to get the parameter for.
            param: The parameter to retrieve.

        Returns:
            The parameter value.

        Raises:
            KeyError: If the parameter doesn't exist.
        """
        return self.StateParams(user)[param]

    def _GetParamOrDefault(self,
                           user: pyrogram.types.User,
                           param: UserMenuParams,
                           def_val: Any) -> Any:
        """
        Get a parameter value or a default if it doesn't exist.

        Args:
            user: The user to get the parameter for.
            param: The parameter to retrieve.
            def_val: The default value if parameter doesn't exist.

        Returns:
            The parameter value or the default value.
        """
        try:
            return self._GetParam(user, param)
        except KeyError:
            return def_val

    def _SetParams(self,
                   user: pyrogram.types.User,
                   **kwargs: Any) -> None:
        """
        Set parameters for a user, clearing existing ones.

        Args:
            user: The user to set parameters for.
            **kwargs: Key-value pairs to set as parameters.
        """
        self.StateParams(user).Clear()
        self._AddParams(user, **kwargs)

    @abstractmethod
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the state implementation.

        Args:
            user: The user executing the state.
            input_data: Input data from user interaction.

        Returns:
            The next menu state type to transition to.
        """
        pass

    @abstractmethod
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the state implementation.

        Args:
            chat: The chat to display content in.
            user: The user viewing the state.
        """
        pass
