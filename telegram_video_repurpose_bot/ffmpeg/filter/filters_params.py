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

from typing import Any, Dict

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.ffmpeg.filter.filter_list import FilterList, FilterTypes


class FilterParams:
    """Filters parameters data structure."""

    config: ConfigObject
    params: Dict[str, Any]

    def __init__(self,
                 config: ConfigObject,
                 params: Dict[str, Any]) -> None:
        """
        Constructor.

        Args:
            config: Configuration object.
            params: Filter parameters dictionary.
        """
        self.config = config
        self.params = params

    def Get(self,
            name: str) -> Any:
        """
        Get parameter by name.

        Args:
            name: Parameter name.

        Returns:
            Parameter value.
        """
        return self.params.get(name)

    def ToString(self) -> str:
        """
        Convert to string.

        Returns:
            String representation of filter parameters.
        """
        msg = ""

        msg += "\nVIDEO\n"
        msg += self.__FiltersToStr(FilterTypes.VIDEO)
        msg += "\n\nAUDIO\n"
        msg += self.__FiltersToStr(FilterTypes.AUDIO)

        return msg.strip()

    def __str__(self) -> str:
        """
        Convert to string.

        Returns:
            String representation of filter parameters.
        """
        return self.ToString()

    def __FiltersToStr(self,
                       filter_type: FilterTypes) -> str:
        """
        Convert filters of a specific type to string.

        Args:
            filter_type: Filter type.

        Returns:
            String representation of filters.
        """
        msg = []
        for filter_cls in FilterList.GetByType(filter_type):
            filter_inst = filter_cls(self.config)
            name = filter_inst.Name()

            val_str = self.params.get(name) if filter_inst.IsEnabled() else "disabled"
            msg.append(f"{name}: {val_str}")

        return "\n".join(msg)
