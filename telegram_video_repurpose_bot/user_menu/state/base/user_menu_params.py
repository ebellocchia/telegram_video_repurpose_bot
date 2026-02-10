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

from enum import Enum, unique


@unique
class UserMenuParams(Enum):
    """
    Enumeration of parameter keys used in user menu state data.

    Defines all state parameters including sentence IDs, video file paths,
    processing results, and elapsed time tracking for menu state flow.
    """

    CONFIG_FILTER_TOGGLE = "config_filter_toggle"
    CONFIG_FILTER_TYPE = "config_filter_type"
    CONFIG_FILTER_CLASS = "config_filter_class"
    CONFIG_FILTER_PARAM_NAME = "config_filter_param_name"
    CONFIG_FILTER_PARAM_SET_ERR = "config_filter_param_set_err"
    CONFIG_FILTER_SEND_ERR = "config_filter_send_err"
    SENTENCE_ARGS = "sentence_args"
    SENTENCE_ID = "sentence_id"
    VIDEO_URL = "video_url"
    VIDEO_ORIG_FILE_NAME = "video_orig_file_name"
    VIDEO_PROC_FILE_NAME = "video_proc_file_name"
    VIDEO_PROC_PARAMS = "video_proc_params"
    VIDEO_PROC_ELAPSED_TIME = "video_proc_elapsed_time"
