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

from __future__ import annotations

from typing import Any

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.ffmpeg.filter.filter_list import FilterList, FilterTypes
from telegram_video_repurpose_bot.ffmpeg.filter.filters_params import FilterParams


class AudioFilterApplier:
    """Audio filter applier class."""

    config: ConfigObject
    filter_params: FilterParams
    stream: Any

    def __init__(self,
                 config: ConfigObject,
                 stream: Any,
                 filter_params: FilterParams) -> None:
        """
        Constructor.

        Args:
            config: Configuration object.
            stream: Audio stream to apply filters to.
            filter_params: Filter parameters.
        """
        self.config = config
        self.filter_params = filter_params
        self.stream = stream

    def ApplyAll(self) -> AudioFilterApplier:
        """
        Apply all filters.

        Returns:
            AudioFilterApplier instance with all filters applied.
        """
        stream = self.stream
        for filter_cls in FilterList.GetByType(FilterTypes.AUDIO):
            filter_inst = filter_cls(self.config)
            params = self.filter_params.Get(filter_inst.Name())
            stream = filter_inst.Apply(stream, params)

        return AudioFilterApplier(self.config, stream, self.filter_params)

    def Stream(self) -> Any:
        """
        Get stream.

        Returns:
            Audio stream with filters applied.
        """
        return self.stream
