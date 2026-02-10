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

from enum import Enum, auto
from typing import Dict, List, Optional, Type

from telegram_video_repurpose_bot.ffmpeg.filter.abitrate_filter import ABitrateFilter
from telegram_video_repurpose_bot.ffmpeg.filter.acontrast_filter import AContrastFilter
from telegram_video_repurpose_bot.ffmpeg.filter.aecho_filter import AEchoFilter
from telegram_video_repurpose_bot.ffmpeg.filter.atempo_filter import ATempoFilter
from telegram_video_repurpose_bot.ffmpeg.filter.colorbalance_filter import ColorbalanceFilter
from telegram_video_repurpose_bot.ffmpeg.filter.colorcorrect_filter import ColorcorrectFilter
from telegram_video_repurpose_bot.ffmpeg.filter.crop_filter import CropFilter
from telegram_video_repurpose_bot.ffmpeg.filter.eq_filter import EqFilter
from telegram_video_repurpose_bot.ffmpeg.filter.filter_base import FilterBase
from telegram_video_repurpose_bot.ffmpeg.filter.fps_filter import FpsFilter
from telegram_video_repurpose_bot.ffmpeg.filter.hflip_filter import HflipFilter
from telegram_video_repurpose_bot.ffmpeg.filter.noise_filter import NoiseFilter
from telegram_video_repurpose_bot.ffmpeg.filter.output_format_filter import OutputFormatFilter
from telegram_video_repurpose_bot.ffmpeg.filter.scale_filter import ScaleFilter
from telegram_video_repurpose_bot.ffmpeg.filter.smartblur_filter import SmartblurFilter
from telegram_video_repurpose_bot.ffmpeg.filter.tempo_filter import TempoFilter
from telegram_video_repurpose_bot.ffmpeg.filter.vbitrate_filter import VBitrateFilter


class FilterTypes(Enum):
    """Enumerations of filter types."""
    AUDIO = auto()
    VIDEO = auto()


class FilterListConst:
    """Constants for filter list."""

    MAP_BY_TYPE: Dict[FilterTypes, List[Type[FilterBase]]] = {
        FilterTypes.VIDEO: [
            FpsFilter,
            HflipFilter,
            TempoFilter,
            EqFilter,
            ColorcorrectFilter,
            ColorbalanceFilter,
            ScaleFilter,
            CropFilter,
            SmartblurFilter,
            NoiseFilter,
            OutputFormatFilter,
            VBitrateFilter,
        ],
        FilterTypes.AUDIO: [
            AContrastFilter,
            AEchoFilter,
            ATempoFilter,
            ABitrateFilter,
        ],
    }


class FilterList:
    """Class for filter list."""

    @staticmethod
    def GetByName(filter_name: str) -> Optional[Type[FilterBase]]:
        """
        Gets filter class for given filter name.

        The filter is searched in the list of available filter classes by name.
        This is not an efficient implementation, but this function is only used for configuring
        filter parameters, so there is no performance constraint.

        Args:
            filter_name: Filter name.

        Returns:
            Filter class for given filter name.
        """
        for filter_type in FilterTypes:
            filters_list = FilterList.GetByType(filter_type)
            filter_cls = next((f for f in filters_list if f.Name() == filter_name), None)
            if filter_cls:
                return filter_cls
        return None

    @staticmethod
    def GetByType(filter_type: FilterTypes) -> List[Type[FilterBase]]:
        """
        Gets filter list for given filter type.

        Args:
            filter_type: Filter type.

        Returns:
            Filter list for given filter type.
        """
        return FilterListConst.MAP_BY_TYPE.get(filter_type, [])
