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

from abc import ABC
from enum import Enum, auto
from typing import Callable, Union

from telegram_video_repurpose_bot.command.command_base import CommandBase
from telegram_video_repurpose_bot.command.command_data import CommandParameterError
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_types import FfmpegConfigTypes


class ParamValueTypes(Enum):
    """Enumeration of parameter value types."""

    FLOAT = auto()
    INTEGER = auto()
    STRING = auto()


class ParamSetterCmdBase(CommandBase, ABC):
    """Abstract base class for parameter setter commands."""

    async def _SetParamMinMaxVal(self,
                                 ffmpeg_config: ConfigObject,
                                 val_type: ParamValueTypes,
                                 min_val_cfg: FfmpegConfigTypes,
                                 max_val_cfg: FfmpegConfigTypes,
                                 is_valid_fct: Callable[[Union[int, float, str], Union[int, float, str]], bool]) -> None:
        """
        Set minimum/maximum parameter value.

        Args:
            ffmpeg_config: FFmpeg configuration object
            val_type: Parameter value type
            min_val_cfg: Minimum value configuration type
            max_val_cfg: Maximum value configuration type
            is_valid_fct: Validation function
        """
        try:
            min_val: Union[int, float, str]
            max_val: Union[int, float, str]

            if val_type == ParamValueTypes.INTEGER:
                min_val = self.cmd_data.Params().GetAsInt(0)
                max_val = self.cmd_data.Params().GetAsInt(1)
            elif val_type == ParamValueTypes.FLOAT:
                min_val = self.cmd_data.Params().GetAsFloat(0)
                max_val = self.cmd_data.Params().GetAsFloat(1)
            else:
                raise CommandParameterError
        except CommandParameterError:
            await self._SendMessage(self.translator.GetSentence("CMD_PARAM_ERR_MSG"))
        else:
            if not is_valid_fct(min_val, max_val) or min_val > max_val:
                await self._SendMessage(self.translator.GetSentence("CMD_PARAM_OUT_OF_RANGE_ERR_MSG"))
                return

            ffmpeg_config.SetValue(min_val_cfg, min_val)
            ffmpeg_config.SetValue(max_val_cfg, max_val)

            await self._SendMessage(
                self.translator.GetSentence("PARAM_MIN_MAX_SET_CMD",
                                            min_val=min_val,
                                            max_val=max_val)
            )

    async def _SetParamVal(self,
                           ffmpeg_config: ConfigObject,
                           val_type: ParamValueTypes,
                           val_cfg: FfmpegConfigTypes,
                           is_valid_fct: Callable[[Union[int, float, str]], bool]) -> None:
        """
        Set parameter value.

        Args:
            ffmpeg_config: FFmpeg configuration object
            val_type: Parameter value type
            val_cfg: Value configuration type
            is_valid_fct: Validation function
        """
        try:
            val: Union[int, float, str]

            if val_type == ParamValueTypes.INTEGER:
                val = self.cmd_data.Params().GetAsInt(0)
            elif val_type == ParamValueTypes.FLOAT:
                val = self.cmd_data.Params().GetAsFloat(0)
            elif val_type == ParamValueTypes.STRING:
                val = self.cmd_data.Params().GetAsString(0)
            else:
                raise CommandParameterError
        except CommandParameterError:
            await self._SendMessage(self.translator.GetSentence("CMD_PARAM_ERR_MSG"))
        else:
            if not is_valid_fct(val):
                await self._SendMessage(self.translator.GetSentence("CMD_PARAM_VAL_ERR_MSG"))
                return

            ffmpeg_config.SetValue(val_cfg, val)

            await self._SendMessage(
                self.translator.GetSentence("PARAM_VALUE_SET_CMD",
                                            val=val)
            )

    async def _SetParamEnabled(self,
                               ffmpeg_config: ConfigObject,
                               val_cfg: FfmpegConfigTypes) -> None:
        """
        Set parameter enabled.

        Args:
            ffmpeg_config: FFmpeg configuration object
            val_cfg: Value configuration type
        """
        try:
            val = self.cmd_data.Params().GetAsBool(0)
        except CommandParameterError:
            await self._SendMessage(self.translator.GetSentence("CMD_PARAM_ERR_MSG"))
        else:
            ffmpeg_config.SetValue(val_cfg, val)

            await self._SendMessage(
                self.translator.GetSentence("PARAM_VALUE_SET_CMD",
                                            val=val)
            )
