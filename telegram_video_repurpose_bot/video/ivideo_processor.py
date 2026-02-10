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
from typing import Tuple

from telegram_video_repurpose_bot.ffmpeg.filter.filters_params import FilterParams


class IVideoProcessor(ABC):
    """
    Interface for video processing implementations.

    Defines the contract for processing video files with filters and
    encoding transformations, returning output file and applied parameters.
    """

    @abstractmethod
    async def ProcessVideo(self,
                           input_file_name: str) -> Tuple[str, FilterParams]:
        """
        Process a video file and apply filters.

        Args:
            input_file_name: The path to the input video file.

        Returns:
            A tuple containing the output file name and the filter parameters used.
        """
        pass
