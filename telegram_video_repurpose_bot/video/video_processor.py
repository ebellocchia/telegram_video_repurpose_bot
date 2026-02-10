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

import asyncio
from typing import Any, Dict, Tuple

import ffmpeg
from typing_extensions import override

from telegram_video_repurpose_bot.bot.bot_config_types import BotConfigTypes
from telegram_video_repurpose_bot.config.config_object import ConfigObject
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_types import FfmpegConfigTypes
from telegram_video_repurpose_bot.ffmpeg.filter.audio_filter_applier import AudioFilterApplier
from telegram_video_repurpose_bot.ffmpeg.filter.filters_params import FilterParams
from telegram_video_repurpose_bot.ffmpeg.filter.filters_params_generator import FilterParamsGenerator
from telegram_video_repurpose_bot.ffmpeg.filter.video_filter_applier import VideoFilterApplier
from telegram_video_repurpose_bot.logger.logger import Logger
from telegram_video_repurpose_bot.utils.utils import RandomUtils
from telegram_video_repurpose_bot.video.ivideo_processor import IVideoProcessor
from telegram_video_repurpose_bot.video.video_processor_ex import VideoProcessError


class VideoProcessorConst:
    """Constants for video processor class."""

    OUTPUT_FILE_NAME_LEN: int = 24


class VideoProcessor(IVideoProcessor):
    """
    Processes video files applying filters and encoding transformations.

    Handles the core video processing pipeline including audio and video stream
    processing with configurable filters, bitrate parameters, and output generation.
    """

    bot_config: ConfigObject
    ffmpeg_config: ConfigObject
    ffmpeg_semaphore: asyncio.Semaphore
    logger: Logger
    params_generator: FilterParamsGenerator

    def __init__(self,
                 bot_config: ConfigObject,
                 ffmpeg_config: ConfigObject,
                 ffmpeg_semaphore: asyncio.Semaphore,
                 logger: Logger) -> None:
        """
        Initialize the video processor.

        Args:
            bot_config: Bot configuration object.
            ffmpeg_config: FFmpeg configuration object.
            logger: The logger instance.
        """
        self.bot_config = bot_config
        self.ffmpeg_config = ffmpeg_config
        self.ffmpeg_semaphore = ffmpeg_semaphore
        self.logger = logger
        self.params_generator = FilterParamsGenerator(ffmpeg_config)

    @override
    async def ProcessVideo(self,
                           input_file_name: str) -> Tuple[str, FilterParams]:
        """
        Process a video file applying filters and encoding.

        Args:
            input_file_name: The path to the input video file.

        Returns:
            A tuple containing the output file name and the filter parameters used.

        Raises:
            VideoProcessError: If video processing fails.
        """
        output_file_name = self.__GenerateOutputFileName()
        self.logger.GetLogger().info(f"Processing video, output file name: {output_file_name}")

        params = self.params_generator.Generate()
        self.logger.GetLogger().info(f"Generated parameters:\n{params}")

        try:
            async with self.ffmpeg_semaphore:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None,
                    self.__RunFFmpeg,
                    input_file_name,
                    output_file_name,
                    params
                )
        except ffmpeg.Error as ex:
            raise VideoProcessError() from ex

        return output_file_name, params

    def __RunFFmpeg(self,
                    input_file_name: str,
                    output_file_name: str,
                    params: FilterParams) -> None:
        """
        Run FFmpeg processing.

        Args:
            input_file_name: The path to the input video file.
            output_file_name: The path to the output video file.
            params: The filter parameters to apply.
        """
        ffmpeg.output(
            self.__ProcessVideo(input_file_name, params),
            self.__ProcessAudio(input_file_name, params),
            output_file_name,
            **self.__GetBitrateParams(params),
            sws_flags=self.ffmpeg_config.GetValue(FfmpegConfigTypes.FFMPEG_SCALE_ALGO),
            vcodec=self.ffmpeg_config.GetValue(FfmpegConfigTypes.FFMPEG_OUTPUT_FORMAT),
            loglevel=self.ffmpeg_config.GetValue(FfmpegConfigTypes.FFMPEG_VERBOSITY)
        ).overwrite_output().run()

    def __ProcessAudio(self,
                       input_file_name: str,
                       filter_params: FilterParams) -> Any:
        """
        Process audio stream with filters.

        Args:
            input_file_name: The path to the input video file.
            filter_params: The filter parameters to apply.

        Returns:
            The processed audio stream.
        """
        return AudioFilterApplier(
            self.ffmpeg_config,
            ffmpeg.input(input_file_name).audio,
            filter_params
        ).ApplyAll().Stream()

    def __ProcessVideo(self,
                       input_file_name: str,
                       filter_params: FilterParams) -> Any:
        """
        Process video stream with filters.

        Args:
            input_file_name: The path to the input video file.
            filter_params: The filter parameters to apply.

        Returns:
            The processed video stream.
        """
        return VideoFilterApplier(
            self.ffmpeg_config,
            ffmpeg.input(input_file_name).video,
            filter_params
        ).ApplyAll().Stream()

    def __GetBitrateParams(self,
                           filter_params: FilterParams) -> Dict[str, int]:
        """
        Get bitrate parameters for video and audio encoding.

        Args:
            filter_params: The filter parameters containing bitrate information.

        Returns:
            A dictionary of bitrate parameters for ffmpeg.
        """
        bitrate_params = {}
        if self.ffmpeg_config.GetValue(FfmpegConfigTypes.FFMPEG_ABITRATE_ENABLED):
            bitrate_params["audio_bitrate"] = filter_params.Get("abitrate")
        if self.ffmpeg_config.GetValue(FfmpegConfigTypes.FFMPEG_VBITRATE_ENABLED):
            bitrate_params["video_bitrate"] = filter_params.Get("vbitrate")
        return bitrate_params

    def __GenerateOutputFileName(self) -> str:
        """
        Generate a random output file name.

        Returns:
            The generated output file path with random name.
        """
        process_folder = self.bot_config.GetValue(BotConfigTypes.VIDEO_PROCESS_FOLDER)
        random_str = RandomUtils.RandomString(VideoProcessorConst.OUTPUT_FILE_NAME_LEN)
        return f"{process_folder}/{random_str}.mp4"
