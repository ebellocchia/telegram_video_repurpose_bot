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
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type, Union

from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_types import FfmpegConfigTypes
from telegram_video_repurpose_bot.utils.utils import RandomUtils


FilterParamSingleValue = Union[float, int, str]
FilterParamMultipleValues = Dict[str, FilterParamSingleValue]
FilterParamValues = Union[FilterParamSingleValue, FilterParamMultipleValues]


@dataclass(frozen=True)
class FilterRandomParamLimit:
    """Represents a filter parameter limit."""

    cfg_type: FfmpegConfigTypes
    limit: Optional[Union[int, float]] = None


@dataclass(frozen=True)
class FilterRandomParamInfo:
    """Represents a filter parameter that have a random value."""

    min: FilterRandomParamLimit
    max: FilterRandomParamLimit
    param_type: Union[Type[int], Type[float]]
    # Precision for float
    precision: int = 3
    # In some filters, multiple parameters are configured by one configuration parameter (i.e. they'll share the same value)
    # In this case, this field is used to map the configuration parameter to the actual FFmpeg parameters
    # For example:
    #   ffmpeg_params_map = ["param_1", "param_2", "param_3"]
    #   rnd_val = RandomUtils.RandomInteger(GetValue(min.cfg_type), GetValue(max.cfg_type))
    # The actual FFmpeg parameters will be:
    # {"param_1": rnd_val, "param_2": rnd_val, "param_3": rnd_val}
    ffmpeg_params_map: List[str] = field(default_factory=list)
    # Function to be called for converting from/to raw value
    conv_from_raw_fct: Callable[[FilterParamSingleValue], FilterParamSingleValue] = lambda v: v
    conv_to_raw_fct: Callable[[FilterParamSingleValue], FilterParamSingleValue] = lambda v: v


@dataclass(frozen=True)
class FilterFixedParamInfo:
    """Represents a filter parameter that have a fixed value."""

    cfg_type: FfmpegConfigTypes
    param_type: Union[Type[int], Type[float], Type[str]]
    limit_str: str
    valid_fct: Callable[[Any], bool]


FilterParamsInfo = Union[
    Dict[str, Union[FilterFixedParamInfo, FilterRandomParamInfo]],  # Filters with multiple named parameters
    FilterFixedParamInfo,                                           # Filters with single unnamed fixed parameter
    FilterRandomParamInfo                                           # Filters with single unnamed random parameter
]


class FilterBase(ABC):
    """Filter base class."""

    config: ConfigObject

    def __init__(self,
                 config: ConfigObject) -> None:
        """
        Constructor.

        Args:
            config: Configuration object
        """
        self.config = config

    @staticmethod
    def CanBeApplied() -> bool:
        """
        Get if the filter can be applied to a stream.

        Returns:
            True if it can be applied, false otherwise.
        """
        return True

    def Apply(self,
              stream: Any,
              params: Any) -> Any:
        """
        Apply filter.

        Args:
            stream: Stream to apply filter to.
            params: Filter parameters.

        Returns:
            Stream with filter applied.
        """
        if not self.IsEnabled() or not self.CanBeApplied():
            return stream

        if isinstance(params, dict):
            return stream.filter(self.Name(), **params)
        if params is None:
            return stream.filter(self.Name())
        return stream.filter(self.Name(), params)

    @classmethod
    def IsValidParameter(cls,
                         *args: Any,
                         **kwargs: Any) -> bool:
        """
        Get if parameter is valid.

        Args:
            *args: Positional arguments for validation.
            **kwargs: Keyword arguments for validation.

        Returns:
            True if parameter is valid, False otherwise.
        """
        params_info = cls.GetParametersInfo()
        if not params_info:
            return True
        # Single parameter
        if isinstance(params_info, (FilterFixedParamInfo, FilterRandomParamInfo)):
            return cls.__IsValidParameterValue(params_info, args[0])
        # Multiple parameters
        for param_name, param_info in params_info.items():
            if param_name not in kwargs:
                continue
            return cls.__IsValidParameterValue(param_info, kwargs[param_name])
        raise ValueError("Invalid parameter name")

    def IsEnabled(self) -> bool:
        """
        Get if filter is enabled.

        Returns:
            True if enabled, False otherwise.
        """
        enable_flag = self.GetEnabledFlag()
        if enable_flag is None:
            return True
        return self.config.GetValue(enable_flag)

    @classmethod
    def ToRawValue(cls,
                   param_name: str,
                   param_val: FilterParamSingleValue) -> FilterParamSingleValue:
        """
        Convert a parameter value to its raw representation.

        Args:
            param_name: Parameter name (empty string for single unnamed parameters)
            param_val: Parameter value to convert

        Returns:
            Converted parameter value in raw format

        Raises:
            ValueError: If filter has no parameters, invalid parameter name, or invalid parameter structure
        """
        params_info = cls.GetParametersInfo()
        # Errors
        if not params_info:
            raise ValueError("Filter has no parameter")
        if param_name and isinstance(params_info, (FilterFixedParamInfo, FilterRandomParamInfo)):
            raise ValueError("Filter has no named parameters")
        # Single fixed parameter (return as it is)
        if isinstance(params_info, FilterFixedParamInfo):
            return param_val
        # Single random parameter (convert and return)
        if isinstance(params_info, FilterRandomParamInfo):
            return params_info.conv_to_raw_fct(param_val)
        # Multiple fixed/random parameters
        if param_name not in params_info.keys():
            raise ValueError(f"Filter has no parameter named {param_name}")
        param_info = params_info[param_name]
        return param_info.conv_to_raw_fct(param_val) if isinstance(param_info, FilterRandomParamInfo) else param_val

    @classmethod
    def FromRawValue(cls,
                     param_name: str,
                     param_val: FilterParamSingleValue) -> FilterParamSingleValue:
        """
        Convert a raw parameter value to its processed representation.

        Args:
            param_name: Parameter name (empty string for single unnamed parameters)
            param_val: Raw parameter value to convert

        Returns:
            Converted parameter value in processed format

        Raises:
            ValueError: If filter has no parameters, invalid parameter name, or invalid parameter structure
        """
        params_info = cls.GetParametersInfo()
        # No parameters
        if not params_info:
            raise ValueError("Filter has no parameter")
        if param_name and isinstance(params_info, (FilterFixedParamInfo, FilterRandomParamInfo)):
            raise ValueError("Filter has no named parameters")
        # Single fixed parameter (return as it is)
        if isinstance(params_info, FilterFixedParamInfo):
            return param_val
        # Single random parameter (convert and return)
        if isinstance(params_info, FilterRandomParamInfo):
            return params_info.conv_from_raw_fct(param_val)
        # Multiple fixed/random parameters
        if param_name not in params_info.keys():
            raise ValueError(f"Filter has no parameter named {param_name}")
        param_info = params_info[param_name]
        return param_info.conv_from_raw_fct(param_val) if isinstance(param_info, FilterRandomParamInfo) else param_val

    def GenerateParameters(self) -> Optional[FilterParamValues]:
        """
        Generate parameters.

        Returns:
            Generated filter parameters.
        """
        params_info = self.GetParametersInfo()
        # No parameters
        if not params_info:
            return None
        # Single fixed parameter
        if isinstance(params_info, FilterFixedParamInfo):
            return self.config.GetValue(params_info.cfg_type)
        # Single random parameter
        if isinstance(params_info, FilterRandomParamInfo):
            return self.__GenerateRandomParameterValue(params_info)
        # Multiple fixed/random parameters
        params_dict = {}
        for param_name, param_info in params_info.items():
            if isinstance(param_info, FilterFixedParamInfo):
                params_dict[param_name] = self.config.GetValue(param_info.cfg_type)
            else:
                param_val = self.__GenerateRandomParameterValue(param_info)
                if isinstance(param_val, dict):
                    params_dict = {**params_dict, **param_val}
                else:
                    params_dict[param_name] = param_val
        return params_dict

    @staticmethod
    def __IsValidParameterValue(param_info: Union[FilterFixedParamInfo, FilterRandomParamInfo],
                                value: Any) -> bool:
        """
        Get if a parameter value is valid.

        Args:
            param_info: Parameter info object.
            value: Value to be checked.

        Returns:
            True if parameter is valid, False otherwise.
        """
        # Fixed parameter
        if isinstance(param_info, FilterFixedParamInfo):
            if not isinstance(value, param_info.param_type):
                return False
            return param_info.valid_fct(value)
        # Random parameter (min/max)
        if isinstance(param_info, FilterRandomParamInfo):
            if not isinstance(value, param_info.param_type):
                return False
            if param_info.min.limit is None and param_info.max.limit is None:
                return True
            if param_info.max.limit is None:
                return value >= param_info.min.limit
            if param_info.min.limit is None:
                return value <= param_info.max.limit
            return param_info.min.limit <= value <= param_info.max.limit

    def __GenerateRandomParameterValue(self,
                                       param_info: FilterRandomParamInfo) -> Any:
        """
        Generate a random value for a filter parameter.

        Args:
            param_info: Filter parameter info object.

        Returns:
            Generated random value.
        """
        val: Union[int, float]
        if param_info.param_type is int:
            val = RandomUtils.RandomInteger(self.config.GetValue(param_info.min.cfg_type),
                                            self.config.GetValue(param_info.max.cfg_type))
        elif param_info.param_type is float:
            val = RandomUtils.RandomFloat(self.config.GetValue(param_info.min.cfg_type),
                                          self.config.GetValue(param_info.max.cfg_type),
                                          param_info.precision)
        else:
            raise ValueError("Invalid parameter type")
        if param_info.ffmpeg_params_map:
            return {
               param_name: param_info.conv_from_raw_fct(val) for param_name in param_info.ffmpeg_params_map
            }
        return param_info.conv_from_raw_fct(val)

    @staticmethod
    @abstractmethod
    def Name() -> str:
        """
        Get filter name.

        Returns:
            Filter name.
        """

    @staticmethod
    @abstractmethod
    def GetEnabledFlag() -> Optional[FfmpegConfigTypes]:
        """
        Get the filter enabled flag.

        Returns:
            Filter enabled flag, None if filter cannot be enabled/disabled.
        """

    @staticmethod
    @abstractmethod
    def GetParametersInfo() -> Optional[FilterParamsInfo]:
        """
        Get supported parameters info.

        Returns:
            List of supported parameters info, None if no parameters.
        """
