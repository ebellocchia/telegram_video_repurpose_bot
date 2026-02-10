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

import logging
import os
from pathlib import Path

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.config.config_typing import ConfigSectionsType
from telegram_video_repurpose_bot.misc.helpers import UserHelper
from telegram_video_repurpose_bot.utils.key_value_converter import KeyValueConverter
from telegram_video_repurpose_bot.utils.utils import Utils


LoggingLevelConverter = KeyValueConverter({
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
})

BotConfig: ConfigSectionsType = {
    # Pyrogram
    "pyrogram": [
        {
            "type": BotConfigTypes.API_ID,
            "name": "api_id",
        },
        {
            "type": BotConfigTypes.API_HASH,
            "name": "api_hash",
        },
        {
            "type": BotConfigTypes.BOT_TOKEN,
            "name": "bot_token",
        },
        {
            "type": BotConfigTypes.SESSION_NAME,
            "name": "session_name",
        },
    ],
    # App
    "app": [
        {
            "type": BotConfigTypes.APP_SUPPORT,
            "name": "app_support",
            "valid_if": lambda cfg, val: UserHelper.IsValidUsername(val),
            "conv_fct": UserHelper.CleanUsername,
        },
        {
            "type": BotConfigTypes.APP_ADMIN_USERS,
            "name": "app_admin_users",
            "valid_if": lambda cfg, val: all(UserHelper.IsValidUsername(u) for u in val),
            "conv_fct": lambda val: set(map(UserHelper.CleanUsername, Utils.StrToStrList(val))),
        },
        {
            "type": BotConfigTypes.APP_AUTH_USERS,
            "name": "app_auth_users",
            "def_val": set(),
            "valid_if": lambda cfg, val: all(UserHelper.IsValidUsername(u) for u in val),
            "conv_fct": lambda val: set(map(UserHelper.CleanUsername, Utils.StrToStrList(val))),
        },
        {
            "type": BotConfigTypes.APP_LANG_FILE,
            "name": "app_lang_file",
            "def_val": None,
        },
    ],
    # Video
    "video": [
        {
            "type": BotConfigTypes.VIDEO_MAX_PROCESSES,
            "name": "video_max_processes",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: val > 0,
        },
        {
            "type": BotConfigTypes.VIDEO_DOWNLOAD_FOLDER,
            "name": "video_download_folder",
            "conv_fct": lambda val: os.path.join(Path(val), ""),    # Clean path and ensure it ends with a slash
            "def_val": "video/download",
            "valid_if": lambda cfg, val: Path(val).exists(),
        },
        {
            "type": BotConfigTypes.VIDEO_DOWNLOAD_DELETE_FILE,
            "name": "video_download_delete_file",
            "conv_fct": Utils.StrToBool,
            "def_val": True,
        },
        {
            "type": BotConfigTypes.VIDEO_PROCESS_FOLDER,
            "name": "video_process_folder",
            "conv_fct": lambda val: os.path.join(Path(val), ""),    # Clean path and ensure it ends with a slash
            "def_val": "video/proc",
            "valid_if": lambda cfg, val: Path(val).exists(),
        },
        {
            "type": BotConfigTypes.VIDEO_PROCESS_DELETE_FILE,
            "name": "video_process_delete_file",
            "conv_fct": Utils.StrToBool,
            "def_val": True,
        },
        {
            "type": BotConfigTypes.VIDEO_FFMPEG_PARAMS_FILE,
            "name": "video_ffmpeg_params_file",
            "def_val": "conf/ffmpeg_params.ini",
            "valid_if": lambda cfg, val: len(val) > 0,
        },
        {
            "type": BotConfigTypes.VIDEO_FFMPEG_FILTERS_DOC_URL,
            "name": "video_ffmpeg_filters_doc_url",
            "def_val": "https://ffmpeg.org/ffmpeg-filters.html",
        },
    ],
    # Logging
    "logging": [
        {
            "type": BotConfigTypes.LOG_LEVEL,
            "name": "log_level",
            "conv_fct": LoggingLevelConverter.KeyToValue,
            "print_fct": LoggingLevelConverter.ValueToKey,
            "def_val": logging.INFO,
        },
        {
            "type": BotConfigTypes.LOG_CONSOLE_ENABLED,
            "name": "log_console_enabled",
            "conv_fct": Utils.StrToBool,
            "def_val": True,
        },
        {
            "type": BotConfigTypes.LOG_FILE_ENABLED,
            "name": "log_file_enabled",
            "conv_fct": Utils.StrToBool,
            "def_val": False,
        },
        {
            "type": BotConfigTypes.LOG_FILE_NAME,
            "name": "log_file_name",
            "load_if": lambda cfg: cfg.GetValue(BotConfigTypes.LOG_FILE_ENABLED),
        },
        {
            "type": BotConfigTypes.LOG_FILE_USE_ROTATING,
            "name": "log_file_use_rotating",
            "conv_fct": Utils.StrToBool,
            "load_if": lambda cfg: cfg.GetValue(BotConfigTypes.LOG_FILE_ENABLED),
        },
        {
            "type": BotConfigTypes.LOG_FILE_APPEND,
            "name": "log_file_append",
            "conv_fct": Utils.StrToBool,
            "load_if": lambda cfg: (cfg.GetValue(BotConfigTypes.LOG_FILE_ENABLED) and
                                    not cfg.GetValue(BotConfigTypes.LOG_FILE_USE_ROTATING)),
        },
        {
            "type": BotConfigTypes.LOG_FILE_MAX_BYTES,
            "name": "log_file_max_bytes",
            "conv_fct": Utils.StrToInt,
            "load_if": lambda cfg: (cfg.GetValue(BotConfigTypes.LOG_FILE_ENABLED) and
                                    cfg.GetValue(BotConfigTypes.LOG_FILE_USE_ROTATING)),
        },
        {
            "type": BotConfigTypes.LOG_FILE_BACKUP_CNT,
            "name": "log_file_backup_cnt",
            "conv_fct": Utils.StrToInt,
            "load_if": lambda cfg: (cfg.GetValue(BotConfigTypes.LOG_FILE_ENABLED) and
                                    cfg.GetValue(BotConfigTypes.LOG_FILE_USE_ROTATING)),
        },
    ],
}
