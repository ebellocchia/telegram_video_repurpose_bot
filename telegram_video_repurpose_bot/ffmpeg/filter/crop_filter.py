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

from typing import Optional

from typing_extensions import override

from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_types import FfmpegConfigTypes
from telegram_video_repurpose_bot.ffmpeg.filter.filter_base import (
    FilterBase,
    FilterParamsInfo,
    FilterRandomParamInfo,
    FilterRandomParamLimit,
)


class CropFilter(FilterBase):
    """Crop filter class."""

    @staticmethod
    @override
    def Name() -> str:
        """
        Get filter name.

        Returns:
            Filter name.
        """
        return "crop"

    @staticmethod
    @override
    def GetParametersInfo() -> Optional[FilterParamsInfo]:
        """
        Get supported parameters info.

        Returns:
            List of supported parameters info, None if no parameters.
        """
        return {
            "h": FilterRandomParamInfo(
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_CROP_H_MIN, 0),
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_CROP_H_MAX),
                int,
                conv_from_raw_fct=lambda v: f"in_h-{v}",
                conv_to_raw_fct=lambda v: v.replace("in_h-", "")    # type: ignore
            ),
            "w": FilterRandomParamInfo(
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_CROP_W_MIN, 0),
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_CROP_W_MAX),
                int,
                conv_from_raw_fct=lambda v: f"in_w-{v}",
                conv_to_raw_fct=lambda v: v.replace("in_w-", "")    # type: ignore
            ),
        }

    @staticmethod
    @override
    def GetEnabledFlag() -> Optional[FfmpegConfigTypes]:
        """
        Get the filter enabled flag.

        Returns:
            Filter enabled flag, None if filter cannot be enabled/disabled.
        """
        return FfmpegConfigTypes.FFMPEG_CROP_ENABLED
