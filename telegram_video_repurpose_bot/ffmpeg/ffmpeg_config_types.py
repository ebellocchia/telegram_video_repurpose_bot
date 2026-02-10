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
class FfmpegConfigTypes(ConfigTypes):
    """FFMPEG configuration types."""
    FFMPEG_ABITRATE_ENABLED = auto()
    FFMPEG_ABITRATE_MIN = auto()
    FFMPEG_ABITRATE_MAX = auto()
    FFMPEG_ACONTRAST_ENABLED = auto()
    FFMPEG_ACONTRAST_MIN = auto()
    FFMPEG_ACONTRAST_MAX = auto()
    FFMPEG_AECHO_ENABLED = auto()
    FFMPEG_AECHO_IN_GAIN_MIN = auto()
    FFMPEG_AECHO_IN_GAIN_MAX = auto()
    FFMPEG_AECHO_OUT_GAIN_MIN = auto()
    FFMPEG_AECHO_OUT_GAIN_MAX = auto()
    FFMPEG_AECHO_DELAYS_MIN = auto()
    FFMPEG_AECHO_DELAYS_MAX = auto()
    FFMPEG_AECHO_DECAYS_MIN = auto()
    FFMPEG_AECHO_DECAYS_MAX = auto()
    # FFMPEG common
    FFMPEG_VERBOSITY = auto()
    FFMPEG_TEMPO_ENABLED = auto()
    FFMPEG_TEMPO_MIN = auto()
    FFMPEG_TEMPO_MAX = auto()
    # FFMPEG video
    FFMPEG_COLORBALANCE_ENABLED = auto()
    FFMPEG_COLORBALANCE_RGBS_MIN = auto()
    FFMPEG_COLORBALANCE_RGBS_MAX = auto()
    FFMPEG_COLORBALANCE_RGBM_MIN = auto()
    FFMPEG_COLORBALANCE_RGBM_MAX = auto()
    FFMPEG_COLORBALANCE_RGBH_MIN = auto()
    FFMPEG_COLORBALANCE_RGBH_MAX = auto()
    FFMPEG_COLORCORRECT_ENABLED = auto()
    FFMPEG_COLORCORRECT_RBL_MIN = auto()
    FFMPEG_COLORCORRECT_RBL_MAX = auto()
    FFMPEG_COLORCORRECT_RBH_MIN = auto()
    FFMPEG_COLORCORRECT_RBH_MAX = auto()
    FFMPEG_CROP_ENABLED = auto()
    FFMPEG_CROP_H_MIN = auto()
    FFMPEG_CROP_H_MAX = auto()
    FFMPEG_CROP_W_MIN = auto()
    FFMPEG_CROP_W_MAX = auto()
    FFMPEG_EQ_ENABLED = auto()
    FFMPEG_EQ_CONTRAST_MIN = auto()
    FFMPEG_EQ_CONTRAST_MAX = auto()
    FFMPEG_EQ_BRIGHTNESS_MIN = auto()
    FFMPEG_EQ_BRIGHTNESS_MAX = auto()
    FFMPEG_EQ_SATURATION_MIN = auto()
    FFMPEG_EQ_SATURATION_MAX = auto()
    FFMPEG_EQ_GAMMA_MIN = auto()
    FFMPEG_EQ_GAMMA_MAX = auto()
    FFMPEG_FPS_ENABLED = auto()
    FFMPEG_FPS_MIN = auto()
    FFMPEG_FPS_MAX = auto()
    FFMPEG_HFLIP_ENABLED = auto()
    FFMPEG_NOISE_ENABLED = auto()
    FFMPEG_NOISE_ALLF = auto()
    FFMPEG_NOISE_ALLS_MIN = auto()
    FFMPEG_NOISE_ALLS_MAX = auto()
    FFMPEG_OUTPUT_FORMAT = auto()
    FFMPEG_SCALE_ENABLED = auto()
    FFMPEG_SCALE_ALGO = auto()
    FFMPEG_SCALE_W = auto()
    FFMPEG_SCALE_H = auto()
    FFMPEG_SMARTBLUR_ENABLED = auto()
    FFMPEG_SMARTBLUR_LR_MIN = auto()
    FFMPEG_SMARTBLUR_LR_MAX = auto()
    FFMPEG_SMARTBLUR_LS_MIN = auto()
    FFMPEG_SMARTBLUR_LS_MAX = auto()
    FFMPEG_SMARTBLUR_LT_MIN = auto()
    FFMPEG_SMARTBLUR_LT_MAX = auto()
    FFMPEG_VBITRATE_ENABLED = auto()
    FFMPEG_VBITRATE_MIN = auto()
    FFMPEG_VBITRATE_MAX = auto()
