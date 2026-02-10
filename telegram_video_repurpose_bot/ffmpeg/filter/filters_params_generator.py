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

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.ffmpeg.filter.atempo_filter import ATempoFilter
from telegram_video_repurpose_bot.ffmpeg.filter.filter_list import FilterList, FilterTypes
from telegram_video_repurpose_bot.ffmpeg.filter.filters_params import FilterParams
from telegram_video_repurpose_bot.ffmpeg.filter.tempo_filter import TempoFilter


class FilterParamsGenerator:
    """Filters parameters generator class."""

    config: ConfigObject

    def __init__(self,
                 config: ConfigObject) -> None:
        """
        Constructor.

        Args:
            config: Configuration object.
        """
        self.config = config

    def Generate(self) -> FilterParams:
        """
        Generate parameters.

        Returns:
            FilterParams object with generated filter parameters.
        """
        params = {}
        for filter_type in FilterTypes:
            for filter_cls in FilterList.GetByType(filter_type):
                filter_inst = filter_cls(self.config)
                params[filter_inst.Name()] = filter_inst.GenerateParameters()

        # Audio and video tempo filters shall be aligned to maintain synchronization
        params[TempoFilter.Name()] = TempoFilter.FromRawValue(
            "",
            ATempoFilter.ToRawValue("", params[ATempoFilter.Name()])    # type: ignore
        )

        return FilterParams(config=self.config, params=params)
