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

from enum import auto, unique

from telegram_video_repurpose_bot.menu.menu_state_types import MenuStateTypes


@unique
class UserMenuStateTypes(MenuStateTypes):
    """
    Enumeration of specific user menu state types.

    Defines all states in the user menu state machine including video processing,
    command display, result display, and menu initialization states.
    """

    CONFIG_INIT = auto()
    CONFIG_MAIN_MENU = auto()
    CONFIG_BOT_ACCESS = auto()
    CONFIG_BOT_ACCESS_ADD = auto()
    CONFIG_BOT_ACCESS_REMOVE = auto()
    CONFIG_FILTER_PARAMS_MANAGE = auto()
    CONFIG_FILTER_ACTION_SELECT = auto()
    CONFIG_FILTER_TYPE_SELECT = auto()
    CONFIG_FILTER_PARAM_TYPE_SELECT = auto()
    CONFIG_FILTER_PARAM_TOGGLE = auto()
    CONFIG_FILTER_PARAM_SET_VALUE = auto()
    INFO_BOT = auto()
    REPURPOSE_VIDEO_INIT = auto()
    REPURPOSE_VIDEO_START = auto()
    REPURPOSE_VIDEO_PROCESS = auto()
    REPURPOSE_VIDEO_SEND = auto()
    REPURPOSE_VIDEO_COMPLETED = auto()
    RESULT = auto()
    START_MENU = auto()
