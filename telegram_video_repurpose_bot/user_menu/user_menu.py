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

from typing import Dict, Type

import pyrogram
from typing_extensions import override

from telegram_video_repurpose_bot.bot.bot_config_manager import BotConfigManager
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_manager import FfmpegConfigManager
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.menu.menu_base import MenuBase
from telegram_video_repurpose_bot.menu.menu_state_params import MenuStateParams
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.translator.translation_loader import TranslationLoader
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase, UserMenuStateBaseInitParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes
from telegram_video_repurpose_bot.user_menu.state.config.config_bot_access_add_state import ConfigBotAccessAddState
from telegram_video_repurpose_bot.user_menu.state.config.config_bot_access_remove_state import ConfigBotAccessRemoveState
from telegram_video_repurpose_bot.user_menu.state.config.config_bot_access_state import ConfigBotAccessState
from telegram_video_repurpose_bot.user_menu.state.config.config_filter_action_select_state import ConfigFilterActionSelectState
from telegram_video_repurpose_bot.user_menu.state.config.config_filter_param_set_value_state import ConfigFilterParamSetValueState
from telegram_video_repurpose_bot.user_menu.state.config.config_filter_param_toggle_state import ConfigFilterParamToggleValueState
from telegram_video_repurpose_bot.user_menu.state.config.config_filter_param_type_select_state import ConfigFilterParamTypeSelectState
from telegram_video_repurpose_bot.user_menu.state.config.config_filter_params_manage_state import ConfigFilterParamsManageState
from telegram_video_repurpose_bot.user_menu.state.config.config_filter_type_select_state import ConfigFilterTypeSelectState
from telegram_video_repurpose_bot.user_menu.state.config.config_init_state import ConfigInitState
from telegram_video_repurpose_bot.user_menu.state.config.config_main_menu_state import ConfigMainMenuState
from telegram_video_repurpose_bot.user_menu.state.others.info_bot_state import InfoBotState
from telegram_video_repurpose_bot.user_menu.state.others.result_state import ResultState
from telegram_video_repurpose_bot.user_menu.state.others.start_menu_state import StartMenuState
from telegram_video_repurpose_bot.user_menu.state.video.repurpose_video_completed import RepurposeVideoCompletedState
from telegram_video_repurpose_bot.user_menu.state.video.repurpose_video_init import RepurposeVideoInitState
from telegram_video_repurpose_bot.user_menu.state.video.repurpose_video_process import RepurposeVideoProcessState
from telegram_video_repurpose_bot.user_menu.state.video.repurpose_video_send import RepurposeVideoSendState
from telegram_video_repurpose_bot.user_menu.state.video.repurpose_video_start import RepurposeVideoStartState


class UserMenuConst:
    """Constants for user menu class."""

    STATES_CLS: Dict[MenuStateTypes, Type[UserMenuStateBase]] = {
        UserMenuStateTypes.CONFIG_INIT: ConfigInitState,
        UserMenuStateTypes.CONFIG_MAIN_MENU: ConfigMainMenuState,
        UserMenuStateTypes.CONFIG_BOT_ACCESS: ConfigBotAccessState,
        UserMenuStateTypes.CONFIG_BOT_ACCESS_ADD: ConfigBotAccessAddState,
        UserMenuStateTypes.CONFIG_BOT_ACCESS_REMOVE: ConfigBotAccessRemoveState,
        UserMenuStateTypes.CONFIG_FILTER_TYPE_SELECT: ConfigFilterTypeSelectState,
        UserMenuStateTypes.CONFIG_FILTER_ACTION_SELECT: ConfigFilterActionSelectState,
        UserMenuStateTypes.CONFIG_FILTER_PARAM_TYPE_SELECT: ConfigFilterParamTypeSelectState,
        UserMenuStateTypes.CONFIG_FILTER_PARAM_TOGGLE: ConfigFilterParamToggleValueState,
        UserMenuStateTypes.CONFIG_FILTER_PARAM_SET_VALUE: ConfigFilterParamSetValueState,
        UserMenuStateTypes.CONFIG_FILTER_PARAMS_MANAGE: ConfigFilterParamsManageState,
        UserMenuStateTypes.INFO_BOT: InfoBotState,
        UserMenuStateTypes.RESULT: ResultState,
        UserMenuStateTypes.START_MENU: StartMenuState,
        UserMenuStateTypes.REPURPOSE_VIDEO_INIT: RepurposeVideoInitState,
        UserMenuStateTypes.REPURPOSE_VIDEO_START: RepurposeVideoStartState,
        UserMenuStateTypes.REPURPOSE_VIDEO_PROCESS: RepurposeVideoProcessState,
        UserMenuStateTypes.REPURPOSE_VIDEO_SEND: RepurposeVideoSendState,
        UserMenuStateTypes.REPURPOSE_VIDEO_COMPLETED: RepurposeVideoCompletedState,
    }


class UserMenu(MenuBase):
    """
    Main user-facing menu for video repurposing interaction.

    Manages user menu states including video processing flow, commands, and
    information display. Initializes all menu states with shared configuration.
    """

    ffmpeg_config_mgr: FfmpegConfigManager

    def __init__(self,
                 client: pyrogram.Client,
                 bot_config_mgr: BotConfigManager,
                 logger: Logger,
                 translator: TranslationLoader) -> None:
        """
        Initialize the user menu.

        Args:
            client: The Pyrogram client instance.
            bot_config_mgr: Bot configuration manager object.
            logger: The logger instance.
            translator: The translation loader instance.
        """
        super().__init__(client, logger)
        self.ffmpeg_config_mgr = FfmpegConfigManager(bot_config_mgr.GetConfig(), logger)
        self.__InitStates(client, bot_config_mgr, logger, translator)

    @staticmethod
    @override
    def _IsCloseQuery(cbk_data: str) -> bool:
        """
        Check if callback data represents a close query.

        Args:
            cbk_data: The callback data to check.

        Returns:
            False, as user menu doesn't support close queries.
        """
        return False

    @override
    def _InitMenuState(self) -> MenuStateTypes:
        """
        Get the initial menu state type.

        Returns:
            The MenuStateTypes value for the start menu state.
        """
        return UserMenuStateTypes.START_MENU

    def __InitStates(self,
                     client: pyrogram.Client,
                     bot_config_mgr: BotConfigManager,
                     logger: Logger,
                     translator: TranslationLoader) -> None:
        """
        Initialize the states of the user menu.

        Args:
            client: The Pyrogram client instance.
            bot_config_mgr: Bot configuration manager object.
            logger: The logger instance.
            translator: The translation loader instance.
        """
        state_params = MenuStateParams()
        for menu_state, state_cls in UserMenuConst.STATES_CLS.items():
            if state_cls is None:
                continue
            self.menu_states_obj[menu_state] = state_cls(
                UserMenuStateBaseInitParams(
                    client,
                    bot_config_mgr,
                    self.ffmpeg_config_mgr,
                    logger,
                    self.menu_message_sender,
                    state_params,
                    translator
                )
            )
