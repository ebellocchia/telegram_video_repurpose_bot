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


class AEchoFilter(FilterBase):
    """Aecho filter class."""

    @staticmethod
    @override
    def Name() -> str:
        """
        Get filter name.

        Returns:
            Filter name.
        """
        return "aecho"

    @staticmethod
    @override
    def GetParametersInfo() -> Optional[FilterParamsInfo]:
        """
        Get supported parameters info.

        Returns:
            List of supported parameters info, None if no parameters.
        """
        return {
            "in_gain": FilterRandomParamInfo(
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_IN_GAIN_MIN, 0.0),
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_IN_GAIN_MAX, 1.0),
                float
            ),
            "out_gain": FilterRandomParamInfo(
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_OUT_GAIN_MIN, 0.0),
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_OUT_GAIN_MAX, 1.0),
                float
            ),
            "delays": FilterRandomParamInfo(
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_DELAYS_MIN, 0.0),
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_DELAYS_MAX, 90_000.0),
                float
            ),
            "decays": FilterRandomParamInfo(
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_DECAYS_MIN, 0.0),
                FilterRandomParamLimit(FfmpegConfigTypes.FFMPEG_AECHO_DECAYS_MAX, 1.0),
                float
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
        return FfmpegConfigTypes.FFMPEG_AECHO_ENABLED
