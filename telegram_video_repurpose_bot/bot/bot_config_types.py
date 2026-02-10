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

from telegram_video_repurpose_bot.config.config_object import ConfigTypes


@unique
class BotConfigTypes(ConfigTypes):
    """Enumeration of bot configuration types."""
    API_ID = auto()
    API_HASH = auto()
    BOT_TOKEN = auto()
    SESSION_NAME = auto()
    # App
    APP_SUPPORT = auto()
    APP_ADMIN_USERS = auto()
    APP_AUTH_USERS = auto()
    APP_LANG_FILE = auto()
    # Video
    VIDEO_MAX_PROCESSES = auto()
    VIDEO_DOWNLOAD_FOLDER = auto()
    VIDEO_DOWNLOAD_DELETE_FILE = auto()
    VIDEO_PROCESS_FOLDER = auto()
    VIDEO_PROCESS_DELETE_FILE = auto()
    VIDEO_FFMPEG_PARAMS_FILE = auto()
    VIDEO_FFMPEG_FILTERS_DOC_URL = auto()
    # Logging
    LOG_LEVEL = auto()
    LOG_CONSOLE_ENABLED = auto()
    LOG_FILE_ENABLED = auto()
    LOG_FILE_NAME = auto()
    LOG_FILE_USE_ROTATING = auto()
    LOG_FILE_APPEND = auto()
    LOG_FILE_MAX_BYTES = auto()
    LOG_FILE_BACKUP_CNT = auto()
