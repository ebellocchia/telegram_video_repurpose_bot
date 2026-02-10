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
from typing import List, Optional, Type, Union

import pyrogram
from typing_extensions import override

from telegram_video_repurpose_bot.callback.callback_query_dispatcher import CallbackQueryTypes
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_manager import FfmpegConfigManager
from telegram_video_repurpose_bot.ffmpeg.filter.filter_base import FilterBase, FilterFixedParamInfo, FilterRandomParamInfo
from telegram_video_repurpose_bot.menu.menu_message_sender import MenuMessageSenderTypes
from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes
from telegram_video_repurpose_bot.user_menu.helper.user_menu_btn_builder import UserMenuBtnTypes
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_params import UserMenuParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_base import UserMenuStateBase, UserMenuStateBaseInitParams
from telegram_video_repurpose_bot.user_menu.state.base.user_menu_state_types import UserMenuStateTypes
from telegram_video_repurpose_bot.utils.utils import Utils


class ConfigFilterParamSetValueState(UserMenuStateBase):
    """Allows to set the value of a filter parameter."""

    ffmpeg_config_mgr: FfmpegConfigManager

    def __init__(self,
                 params: UserMenuStateBaseInitParams) -> None:
        """
        Initialize the configuration filter parameter set state.

        Args:
            params: UserMenuStateBaseInitParams containing initialization parameters.
        """
        super().__init__(params)
        self.ffmpeg_config_mgr = params.ffmpeg_config_mgr

    @staticmethod
    @override
    def WaitsForInput() -> bool:
        """
        Check if the state waits for user input.

        Returns:
            True, the state waits for user input.
        """
        return True

    @override
    async def _Execute(self,
                       user: pyrogram.types.User,
                       input_data: str) -> MenuStateTypes:
        """
        Execute the configuration filter parameter set state logic.

        Args:
            user: The user executing the state.
            input_data: The callback data from user selection.

        Returns:
            The next menu state type based on user input.
        """
        if input_data == CallbackQueryTypes.BACK:
            param_name = self._GetParam(user, UserMenuParams.CONFIG_FILTER_PARAM_NAME)
            if param_name:
                return UserMenuStateTypes.CONFIG_FILTER_PARAM_TYPE_SELECT
            return UserMenuStateTypes.CONFIG_FILTER_TYPE_SELECT

        parsed_values = self.__ParseInputs(user, input_data)
        if not parsed_values:
            self._AddParams(user, config_filter_param_set_err=True)
            return UserMenuStateTypes.CONFIG_FILTER_PARAM_SET_VALUE

        self.__UpdateFilterParamValue(user, parsed_values)
        self._AddParams(user, config_filter_param_set_err=False)
        return UserMenuStateTypes.CONFIG_FILTER_PARAM_SET_VALUE

    @override
    async def _Show(self,
                    chat: pyrogram.types.Chat,
                    user: pyrogram.types.User) -> None:
        """
        Display the filter parameter set menu to the user.

        Args:
            chat: The chat to display the menu in.
            user: The user viewing the menu.
        """
        filter_class = self._GetParam(user, UserMenuParams.CONFIG_FILTER_CLASS)
        param_name = self._GetParam(user, UserMenuParams.CONFIG_FILTER_PARAM_NAME)
        param_val = self.__GetFilterParamValue(user)
        param_lim = self.__GetFilterParamLimit(user)
        is_err = self._GetParam(user, UserMenuParams.CONFIG_FILTER_PARAM_SET_ERR)

        await self.message_sender.SendMessage(
            MenuMessageSenderTypes.SEND_OR_EDIT,
            chat,
            user,
            self.translator.GetSentence("CONFIG_FILTER_PARAM_SET_MSG" if param_name else "CONFIG_FILTER_PARAM_UNNAMED_SET_MSG",
                                        param_name=param_name,
                                        param_lim=param_lim,
                                        param_val=param_val,
                                        filter_name=filter_class.Name(),
                                        err_msg=self.translator.GetSentence("CONFIG_FILTER_PARAM_SET_ERR_MSG") if is_err else ""),
            reply_markup=self.menu_btn_builder.KeyboardMarkupCbk(UserMenuBtnTypes.BACK)
        )

    def __GetFilterParamInfo(self,
                             user: pyrogram.types.User) -> Union[FilterFixedParamInfo, FilterRandomParamInfo]:
        """
        Get the selected filter parameter info.

        Args:
            user: The user viewing the menu.

        Returns:
            The selected parameter info.
        """
        filter_class = self._GetParam(user, UserMenuParams.CONFIG_FILTER_CLASS)
        param_name = self._GetParam(user, UserMenuParams.CONFIG_FILTER_PARAM_NAME)
        return filter_class.GetParametersInfo()[param_name] if param_name else filter_class.GetParametersInfo()

    def __GetFilterParamValue(self,
                              user: pyrogram.types.User) -> str:
        """
        Get the selected filter parameter current value.

        Args:
            user: The user viewing the menu.

        Returns:
            String representing the current filter parameter value.
        """
        ffmpeg_config = self.ffmpeg_config_mgr.GetConfig()
        param_info = self.__GetFilterParamInfo(user)
        if isinstance(param_info, FilterFixedParamInfo):
            return str(ffmpeg_config.GetValue(param_info.cfg_type))
        else:
            param_min_val = ffmpeg_config.GetValue(param_info.min.cfg_type)
            param_max_val = ffmpeg_config.GetValue(param_info.max.cfg_type)
            return f"{param_min_val} - {param_max_val}"

    def __GetFilterParamLimit(self,
                              user: pyrogram.types.User) -> str:
        """
        Get the selected filter parameter limit.

        Args:
            user: The user viewing the menu.

        Returns:
            String representing the filter parameter limit.
        """
        param_info = self.__GetFilterParamInfo(user)
        if isinstance(param_info, FilterFixedParamInfo):
            return param_info.limit_str
        else:
            if param_info.min.limit is None:
                return f"v <= {param_info.max.limit}"
            if param_info.max.limit is None:
                return f"v >= {param_info.min.limit}"
            return f"{param_info.min.limit} <= v <= {param_info.max.limit}"

    def __UpdateFilterParamValue(self,
                                 user: pyrogram.types.User,
                                 new_values: List[Union[int, float, str]]) -> None:
        """
        Update the selected filter parameter value.

        Args:
            user: The user viewing the menu.
            new_values: The new filter parameter value.
        """
        ffmpeg_config = self.ffmpeg_config_mgr.GetConfig()
        param_info = self.__GetFilterParamInfo(user)

        if isinstance(param_info, FilterFixedParamInfo):
            ffmpeg_config.SetValue(param_info.cfg_type, new_values[0])
        elif isinstance(param_info, FilterRandomParamInfo):
            ffmpeg_config.SetValue(param_info.min.cfg_type, new_values[0])
            ffmpeg_config.SetValue(param_info.max.cfg_type, new_values[1])

    def __ParseInputs(self,
                      user: pyrogram.types.User,
                      input_data: str) -> Optional[List[Union[int, float, str]]]:
        """
        Parse input.

        Args:
            user: The user viewing the menu.
            input_data: Input data from user.

        Returns:
            List of parsed values, None in case of error.
        """
        filter_class = self._GetParam(user, UserMenuParams.CONFIG_FILTER_CLASS)
        param_name = self._GetParam(user, UserMenuParams.CONFIG_FILTER_PARAM_NAME)
        param_info = self.__GetFilterParamInfo(user)

        input_parts = input_data.split()
        # Check input length
        if isinstance(param_info, FilterFixedParamInfo) and len(input_parts) != 1:
            self.logger.GetLogger().info("Invalid input parts (too few)")
            return None
        if isinstance(param_info, FilterRandomParamInfo) and len(input_parts) != 2:
            self.logger.GetLogger().info("Invalid input parts (too few)")
            return None

        self.logger.GetLogger().info(f"Parsing input parts: {input_parts}")
        try:
            parsed_values = [self.__ParseValue(filter_class, param_name, param_info.param_type, input_str.strip())
                             for input_str in input_parts]
        except ValueError as e:
            self.logger.GetLogger().info(f"Unable to parse input parts: {e}")
            return None

        # Check min/max
        if isinstance(param_info, FilterRandomParamInfo):
            if parsed_values[0] > parsed_values[1]:     # type: ignore
                self.logger.GetLogger().info("Invalid parsed values (min > max)")
                return None

        self.logger.GetLogger().info(f"Parsed values: {parsed_values}")

        return parsed_values

    @staticmethod
    def __ParseValue(filter_class: Type[FilterBase],
                     param_name: str,
                     param_type: Union[Type[int], Type[float], Type[str]],
                     input_str: str) -> Union[int, float, str]:
        """
        Parse a single input value.

        Args:
            filter_class: The filter class.
            param_name: The parameter name.
            param_type: The parameter type.
            input_str: The input string.

        Returns:
            Parsed value.

        Raises:
            ValueError: If the value cannot be parsed.
        """
        input_val: Union[int, float, str]
        if param_type is int:
            input_val = Utils.StrToInt(input_str)
        elif param_type is float:
            input_val = Utils.StrToFloat(input_str)
        else:
            input_val = input_str

        if param_name:
            is_valid = filter_class.IsValidParameter(**{param_name: input_val})
        else:
            is_valid = filter_class.IsValidParameter(input_val)

        if not is_valid:
            raise ValueError("Invalid parameter value")
        return input_val
