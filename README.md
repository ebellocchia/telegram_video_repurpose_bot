# Telegram Video Repurpose & Uniquing Bot

| |
|---|
| [![PyPI - Version](https://img.shields.io/pypi/v/telegram_video_repurpose_bot.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/telegram_video_repurpose_bot/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/telegram_video_repurpose_bot.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/telegram_video_repurpose_bot/) [![GitHub License](https://img.shields.io/github/license/ebellocchia/telegram_video_repurpose_bot?label=License)](https://github.com/ebellocchia/telegram_video_repurpose_bot?tab=MIT-1-ov-file) |
| [![Build](https://github.com/ebellocchia/telegram_video_repurpose_bot/actions/workflows/build.yml/badge.svg)](https://github.com/ebellocchia/telegram_video_repurpose_bot/actions/workflows/build.yml) [![Code Analysis](https://github.com/ebellocchia/telegram_video_repurpose_bot/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/ebellocchia/telegram_video_repurpose_bot/actions/workflows/code-analysis.yml) |
| [![Codacy Badge](https://app.codacy.com/project/badge/Grade/a81c59455bb44b979f807ef5c96d674f)](https://app.codacy.com/gh/ebellocchia/telegram_video_repurpose_bot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) [![CodeFactor](https://www.codefactor.io/repository/github/ebellocchia/telegram_video_repurpose_bot/badge)](https://www.codefactor.io/repository/github/ebellocchia/telegram_video_repurpose_bot) |
| |

## Introduction

Telegram bot based on *pyrotgfork* (a maintained fork of the *pyrogram* library).

This bot was originally developed as a commissioned project for social media content management.
While the original project is no longer active, this version has been updated and streamlined for public use.

### Project Purpose

The core concept of the bot is video uniquing.

The bot processes an input video and applies subtle *FFmpeg* filters to generate technically unique versions of the same file.
This allows users to post the same content multiple times across different social media accounts (such as TikTok or Instagram) while minimizing the risk of duplicate content flags or automated bans.

### How It Works

Instead of applying static filters, the bot uses a system of controlled randomization:
- The user defines a range (minimum/maximum) for each supported *FFmpeg parameter*.
  
  While the bot currently supports a small subset of filters selected for content uniquing, the codebase is structured to be modular, making it easy to add new filters as needed.
- Every time a video is processed, the bot generates a random value within that specified range for each filter.
- Consequently, every output video is technically unique, even when starting from the same source file.

### Key Features

- User-Friendly Interface: Designed with non-technical users in mind, the bot is fully managed via a button-based GUI.
- Direct Processing: In this version, videos are sent directly to the bot within the Telegram chat (automatic downloading from TikTok/Instagram URLs has been removed to ensure easier maintenance).
- Role-Based Access Control:
    - Administrators: Can manage user permissions (i.e. add/remove creators) and modify the audio/video parameters.
    - Creators: Can only process videos using the pre-configured settings.

### Video Example

<video src="https://github.com/user-attachments/assets/7be57b6c-aa1c-4fcd-9f05-c52722df7a50" width="50%">
</video>

## Setup

### Create Telegram app

In order to use the bot, you need a Telegram bot token, an API ID, and an API hash.

To obtain them, create an app on the following website: [https://my.telegram.org/apps](https://my.telegram.org/apps).

### Installation

This package requires **Python >= 3.7**.

1. **Install FFmpeg:**
The bot requires *FFmpeg* to be installed and available in the system (i.e. added to the system `PATH`).

    Please refer to the [official download page](https://ffmpeg.org/download.html) for installation instructions.

    To verify the installation, open a terminal and run: `ffmpeg -version`

    If the command returns version information, *FFmpeg* is correctly set up. Example output (truncated):

```
ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
```

2. **Set up a virtual environment (optional but recommended)**:

```
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
```

3. **Install the bot:**

```
pip install telegram_video_repurpose_bot
```

**IMPORTANT NOTE:** This bot uses *pyrotgfork*. If you are not using a virtual environment, ensure that the standard *pyrogram* library (or forks) is not installed in your Python environment.
Since both libraries use the same package name, having both installed will cause conflicts and the bot will not function correctly.

4. **Set up the bot:**
Copy the **app** folder from the repository to your device. Edit the configuration file by specifying your API ID, API hash, bot token, and other parameters according to your needs (see the "Configuration" chapter).
5. **Run the bot:**
Inside the **app** folder, launch the **bot_start.py** script to start the bot:

```
python bot_start.py
```

---

#### Custom Configuration

When run without parameters, the bot uses **conf/config.ini** as the default configuration file. To specify a different configuration file, use:

```
python bot_start.py -c another_conf.ini
```

or:

```
python bot_start.py --config another_conf.ini
```

This allows you to manage different bots easily, each one with its own configuration file.

### Code analysis

To run code analysis:

```
mypy .
ruff check .
```

## Configuration

### Bot Configuration

An example of bot configuration file is provided in the *app* folder: **app/conf/config.ini**.

The full list of configurable fields is documented below.

| Name | Description |
| --- | --- |
| **[pyrogram]** | *Configuration for pyrogram* |
| `session_name` | Path of the file used to store the session. |
| `api_id` | API ID from [https://my.telegram.org/apps](https://my.telegram.org/apps). |
| `api_hash` | API hash from [https://my.telegram.org/apps](https://my.telegram.org/apps). |
| `bot_token` | Bot token from *BotFather*. |
| **[app]** | *Configuration for app* |
| `app_support` | Username of the user to contact for support in case of bot errors. |
| `app_admin_users` | List of usernames of admin users (see "User Roles"). |
| `app_auth_users` | List of usernames of authorized users (see "User Roles"). |
| `app_lang_file` | Path of custom language file in XML format (default: English). |
| **[video]** | *Configuration for videos* |
| `video_max_processes` | Maximum number of FFmpeg processes that can be active at the same time. |
| `video_download_folder` | Path of the folder where downloaded videos are stored (default: `video/download/`). Path must be existent, an error will be triggered if not existent. |
| `video_download_delete_file` | True to delete downloaded video, false otherwise (default: `true`) |
| `video_process_folder` | Path of the folder where processed videos are stored (default: `video/proc/`). Path must be existent, an error will be triggered if not existent. |
| `video_process_delete_file` | True to delete processed video, false otherwise (default: `true`) |
| `video_ffmpeg_params_file` | Path of the *ffmpeg* configuration file (default: `conf/ffmpeg_params.ini`). |
| `video_ffmpeg_filters_doc_url` | URL with FFmpeg filter documentation (default: `https://ffmpeg.org/ffmpeg-filters.html`) |
| **[logging]** | *Configuration for logging* |
| `log_level` | Log level, same as python logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default: `INFO`. |
| `log_console_enabled` | True to enable logging to console, false otherwise (default: `true`) |
| `log_file_enabled` | True to enable logging to file, false otherwise (default: `false`). If false, the following fields will be ignored. |
| `log_file_name` | Log file name |
| `log_file_use_rotating` | True to use a rotating log file, false otherwise |
| `log_file_max_bytes` | Maximum size in bytes for a log file. When reached, a new log file is created up to `log_file_backup_cnt`. Only valid if `log_file_use_rotating` is true. |
| `log_file_backup_cnt` | Maximum number of log files. Only valid if `log_file_use_rotating` is true. |
| `log_file_append` | True to append to the log file, false to start fresh each time. Only valid if `log_file_use_rotating` is false. |

### FFmpeg Configuration

The file **app/conf/ffmpeg_params.ini** serves as the baseline for *FFmpeg* configuration.
It contains the default enable flags and ranges (min/max values) for all supported filters.

**NOTE:** Since *FFmpeg* parameters can be updated directly via bot GUI, manual editing of this file is generally unnecessary.

The full list of configurable fields is documented below.

| Parameter | Description |
| --- | --- |
| **[ffmpeg_audio]** | *Audio* |
| `ffmpeg_abitrate_enabled` | Enable/disable audio bitrate control. |
| `ffmpeg_abitrate_min / max` | Target audio bitrate range (in bits/s). |
| `ffmpeg_acontrast_enabled` | Enable/disable the audio contrast filter. |
| `ffmpeg_acontrast_min / max` | Range for audio contrast expansion/compression. |
| `ffmpeg_aecho_enabled` | Enable/disable the audio echo effect. |
| `ffmpeg_aecho_in_gain_min / max` | Range for input signal volume (gain). |
| `ffmpeg_aecho_out_gain_min / max` | Range for output signal volume (gain). |
| `ffmpeg_aecho_delays_min / max` | Range for echo delay in milliseconds. |
| `ffmpeg_aecho_decays_min / max` | Range for echo decay factors. |
| **[ffmpeg_common]** | *Common* |
| `ffmpeg_verbosity` | Verbosity level for FFmpeg (default: `error`), same of FFmpeg `-loglevel`. |
| `ffmpeg_tempo_enabled` | Enable/disable playback speed adjustment (without pitch shift). |
| `ffmpeg_tempo_min / max` | Speed multiplier range (e.g., 0.96x to 1.04x). |
| **[ffmpeg_video]** | *Video* |
| `ffmpeg_colorbalance_enabled` | Enable/disable color balance adjustments. |
| `ffmpeg_colorbalance_rgbs_min / max` | Range for Red, Green, and Blue shadows. |
| `ffmpeg_colorbalance_rgbm_min / max` | Range for Red, Green, and Blue midtones. |
| `ffmpeg_colorbalance_rgbh_min / max` | Range for Red, Green, and Blue highlights. |
| `ffmpeg_colorcorrect_enabled` | Enable/disable the color correction filter. |
| `ffmpeg_colorcorrect_rbl_min / max` | Range for red/blue components in lowlights. |
| `ffmpeg_colorcorrect_rbh_min / max` | Range for red/blue components in highlights. |
| `ffmpeg_crop_enabled` | Enable/disable video cropping. |
| `ffmpeg_crop_h_min / max` | Range for height pixels to be cropped. |
| `ffmpeg_crop_w_min / max` | Range for width pixels to be cropped. |
| `ffmpeg_eq_enabled` | Enable/disable the equalizer (Brightness, Contrast, Saturation, Gamma). |
| `ffmpeg_eq_contrast_min / max` | Range for video contrast adjustment. |
| `ffmpeg_eq_brightness_min / max` | Range for video brightness adjustment. |
| `ffmpeg_eq_saturation_min / max` | Range for color saturation intensity. |
| `ffmpeg_eq_gamma_min / max` | Range for gamma correction. |
| `ffmpeg_fps_enabled` | Enable/disable forced output frame rate (FPS). |
| `ffmpeg_fps_min / max` | Range for target frames per second. |
| `ffmpeg_hflip_enabled` | Enable/disable horizontal flip (mirror effect). |
| `ffmpeg_noise_enabled` | Enable/disable artificial video noise. |
| `ffmpeg_noise_allf` | Noise flags (e.g., `a+p+u` for all planes/uniform noise). |
| `ffmpeg_noise_alls_min / max` | Range for noise seed/intensity. |
| `ffmpeg_output_format` | Defines the output video codec (possible values: `h264`, `libx265`, `h264_nvenc`, `hevc_nvenc`). |
| `ffmpeg_scale_enabled` | Enable/disable video resizing. |
| `ffmpeg_scale_algo` | Scaling algorithm used (possible values: `fast_bilinear`, `bilinear`, `bicubic`, `neighbor`, `area`, `bicublin`, `gauss`, `spline`). |
| `ffmpeg_scale_w / h` | Target output resolution (Width x Height). |
| `ffmpeg_smartblur_enabled` | Enable/disable the smart blur filter. |
| `ffmpeg_smartblur_lr_min / max` | Range for luma radius. |
| `ffmpeg_smartblur_ls_min / max` | Range for luma strength. |
| `ffmpeg_smartblur_lt_min / max` | Range for luma threshold. |
| `ffmpeg_vbitrate_enabled` | Enable/disable video bitrate control. |
| `ffmpeg_vbitrate_min / max` | Target video bitrate range (in bits/s). |

## User Roles

As previously described, the bot implements a simple RBAC (Role-Based Access Control) system to manage usage:

|Feature|Admin Users|Authorized Users|
|---|---|---|
|Process Videos|✅|✅|
|Change *FFmpeg* Parameters|✅|❌|
|Add/Remove Authorized Users|✅|❌|

**Role Details:**
- *Admin Users*: Have total control over the bot instance. They are responsible for configuring the processing engine and managing the access list.
- *Authorized Users*: Can utilize the bot's core functionality (video processing) but cannot alter global settings or manage other users.

## Bot GUI

The bot GUI is intuitive and straightforward. The main menu consists of three primary options:

<img src="https://github.com/ebellocchia/telegram_video_repurpose_bot/blob/main/asset/main_menu.png" width="400px">

- **Process Video**: Start processing a video file.
- **Configure Bot**: Access bot configuration (restricted to administrators).
- **Info Bot**: Display general information about the bot (i.e. author, version).

The configuration menu allows administrators to manage authorized users and adjust FFmpeg parameters:

<img src="https://github.com/ebellocchia/telegram_video_repurpose_bot/blob/main/asset/configure_menu.png" width="300px">

- **Bot Access**: Add, remove, or view authorized users.

<img src="https://github.com/ebellocchia/telegram_video_repurpose_bot/blob/main/asset/bot_access_menu.png" width="300px">

- **Audio Parameters** / **Video Parameters**: Enable, disable, or modify specific FFmpeg filters.

    Both menus share a similar interface, varying only in the available filter list.

| | |
|---|---|
|<img src="https://github.com/ebellocchia/telegram_video_repurpose_bot/blob/main/asset/filter_menu.png" width="250px">|<img src="https://github.com/ebellocchia/telegram_video_repurpose_bot/blob/main/asset/filter_set_menu.png" width="400px">|

- **Parameters Management**: Save, load, or view FFmpeg configurations.

    - **Concept**: Changes made via the GUI are applied in-memory and will be lost if the bot restarts.
    To make changes permanent, they must be saved to file. Similarly, users can load from file to revert unsaved in-memory changes.

<img src="https://github.com/ebellocchia/telegram_video_repurpose_bot/blob/main/asset/parameters_management_menu.png" width="300px">

- **Filters Documentation**: Opens the official FFmpeg documentation for detailed filter descriptions.

## Run the Bot

The bot is designed for use in private chats. There is no need to add it to a group.

To ensure the bot remains online and responsive, it is highly recommended to host it on a VPS for 24/7 operation.

**Note:** While *FFmpeg* is known for being resource-intensive, this bot is specifically intended to process short video clips (1 to 2 minutes).
Therefore, even a low-spec VPS should be sufficient to handle the processing tasks effectively.

### Docker

Docker files are provided to run the bot in a container. You can specify the configuration file via the `CONFIG_FILE` variable:

```
CONFIG_FILE=conf/config.ini docker compose up -d --build
```

## Translation

Bot messages can be translated using a custom XML file specified in the `app_lang_file` field. An Italian example is provided in **app/lang**.

# License

This software is available under the MIT license.
