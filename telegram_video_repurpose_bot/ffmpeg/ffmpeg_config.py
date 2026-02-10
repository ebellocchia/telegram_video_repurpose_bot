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

from telegram_video_repurpose_bot.config.config_typing import ConfigSectionsType
from telegram_video_repurpose_bot.ffmpeg.ffmpeg_config_types import FfmpegConfigTypes
from telegram_video_repurpose_bot.ffmpeg.filter.abitrate_filter import ABitrateFilter
from telegram_video_repurpose_bot.ffmpeg.filter.acontrast_filter import AContrastFilter
from telegram_video_repurpose_bot.ffmpeg.filter.aecho_filter import AEchoFilter
from telegram_video_repurpose_bot.ffmpeg.filter.colorbalance_filter import ColorbalanceFilter
from telegram_video_repurpose_bot.ffmpeg.filter.colorcorrect_filter import ColorcorrectFilter
from telegram_video_repurpose_bot.ffmpeg.filter.crop_filter import CropFilter
from telegram_video_repurpose_bot.ffmpeg.filter.eq_filter import EqFilter
from telegram_video_repurpose_bot.ffmpeg.filter.fps_filter import FpsFilter
from telegram_video_repurpose_bot.ffmpeg.filter.noise_filter import NoiseFilter
from telegram_video_repurpose_bot.ffmpeg.filter.output_format_filter import OutputFormatFilter
from telegram_video_repurpose_bot.ffmpeg.filter.scale_filter import ScaleFilter
from telegram_video_repurpose_bot.ffmpeg.filter.smartblur_filter import SmartblurFilter
from telegram_video_repurpose_bot.ffmpeg.filter.tempo_filter import TempoFilter
from telegram_video_repurpose_bot.ffmpeg.filter.vbitrate_filter import VBitrateFilter
from telegram_video_repurpose_bot.utils.utils import Utils


FfmpegConfig: ConfigSectionsType = {
    # FFMPEG audio
    "ffmpeg_audio": [
        # abitrate
        {
            "type": FfmpegConfigTypes.FFMPEG_ABITRATE_ENABLED,
            "name": "ffmpeg_abitrate_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_ABITRATE_MIN,
            "name": "ffmpeg_abitrate_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: ABitrateFilter.IsValidParameter(val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_ABITRATE_MAX,
            "name": "ffmpeg_abitrate_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (ABitrateFilter.IsValidParameter(val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_ABITRATE_MIN)),
        },
        # acontrast
        {
            "type": FfmpegConfigTypes.FFMPEG_ACONTRAST_ENABLED,
            "name": "ffmpeg_acontrast_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_ACONTRAST_MIN,
            "name": "ffmpeg_acontrast_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: AContrastFilter.IsValidParameter(val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_ACONTRAST_MAX,
            "name": "ffmpeg_acontrast_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (AContrastFilter.IsValidParameter(val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_ACONTRAST_MIN)),
        },
        # aecho
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_ENABLED,
            "name": "ffmpeg_aecho_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_IN_GAIN_MIN,
            "name": "ffmpeg_aecho_in_gain_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: AEchoFilter.IsValidParameter(in_gain=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_IN_GAIN_MAX,
            "name": "ffmpeg_aecho_in_gain_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (AEchoFilter.IsValidParameter(in_gain=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_AECHO_IN_GAIN_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_OUT_GAIN_MIN,
            "name": "ffmpeg_aecho_out_gain_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: AEchoFilter.IsValidParameter(out_gain=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_OUT_GAIN_MAX,
            "name": "ffmpeg_aecho_out_gain_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (AEchoFilter.IsValidParameter(out_gain=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_AECHO_OUT_GAIN_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_DELAYS_MIN,
            "name": "ffmpeg_aecho_delays_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: AEchoFilter.IsValidParameter(delays=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_DELAYS_MAX,
            "name": "ffmpeg_aecho_delays_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (AEchoFilter.IsValidParameter(delays=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_AECHO_DELAYS_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_DECAYS_MIN,
            "name": "ffmpeg_aecho_decays_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: AEchoFilter.IsValidParameter(decays=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_AECHO_DECAYS_MAX,
            "name": "ffmpeg_aecho_decays_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (AEchoFilter.IsValidParameter(decays=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_AECHO_DECAYS_MIN)),
        },
    ],
    # FFMPEG common
    "ffmpeg_common": [
        {
            "type": FfmpegConfigTypes.FFMPEG_VERBOSITY,
            "name": "ffmpeg_verbosity",
            "def_val": "error",
            "valid_if": lambda cfg, val: val in ["quiet", "panic", "fatal", "error", "warning", "info", "verbose"],
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_TEMPO_ENABLED,
            "name": "ffmpeg_tempo_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_TEMPO_MIN,
            "name": "ffmpeg_tempo_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: TempoFilter.IsValidParameter(val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_TEMPO_MAX,
            "name": "ffmpeg_tempo_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (TempoFilter.IsValidParameter(val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_TEMPO_MIN)),
        },
    ],
    # FFMPEG video
    "ffmpeg_video": [
        # colorbalance
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_ENABLED,
            "name": "ffmpeg_colorbalance_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBS_MIN,
            "name": "ffmpeg_colorbalance_rgbs_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: ColorbalanceFilter.IsValidParameter(rgbs=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBS_MAX,
            "name": "ffmpeg_colorbalance_rgbs_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (ColorbalanceFilter.IsValidParameter(rgbs=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBS_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBM_MIN,
            "name": "ffmpeg_colorbalance_rgbm_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: ColorbalanceFilter.IsValidParameter(rgbm=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBM_MAX,
            "name": "ffmpeg_colorbalance_rgbm_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (ColorbalanceFilter.IsValidParameter(rgbm=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBM_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBH_MIN,
            "name": "ffmpeg_colorbalance_rgbh_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: ColorbalanceFilter.IsValidParameter(rgbh=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBH_MAX,
            "name": "ffmpeg_colorbalance_rgbh_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (ColorbalanceFilter.IsValidParameter(rgbh=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_COLORBALANCE_RGBH_MIN)),
        },
        # colorcorrect
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORCORRECT_ENABLED,
            "name": "ffmpeg_colorcorrect_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORCORRECT_RBL_MIN,
            "name": "ffmpeg_colorcorrect_rbl_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: ColorcorrectFilter.IsValidParameter(rbl=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORCORRECT_RBL_MAX,
            "name": "ffmpeg_colorcorrect_rbl_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (ColorcorrectFilter.IsValidParameter(rbl=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_COLORCORRECT_RBL_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORCORRECT_RBH_MIN,
            "name": "ffmpeg_colorcorrect_rbh_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: ColorcorrectFilter.IsValidParameter(rbh=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_COLORCORRECT_RBH_MAX,
            "name": "ffmpeg_colorcorrect_rbh_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (ColorcorrectFilter.IsValidParameter(rbh=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_COLORCORRECT_RBH_MIN)),
        },
        # crop
        {
            "type": FfmpegConfigTypes.FFMPEG_CROP_ENABLED,
            "name": "ffmpeg_crop_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_CROP_H_MIN,
            "name": "ffmpeg_crop_h_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: CropFilter.IsValidParameter(h=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_CROP_H_MAX,
            "name": "ffmpeg_crop_h_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (CropFilter.IsValidParameter(h=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_CROP_H_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_CROP_W_MIN,
            "name": "ffmpeg_crop_w_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: CropFilter.IsValidParameter(w=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_CROP_W_MAX,
            "name": "ffmpeg_crop_w_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (CropFilter.IsValidParameter(w=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_CROP_W_MIN)),
        },
        # eq
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_ENABLED,
            "name": "ffmpeg_eq_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_CONTRAST_MIN,
            "name": "ffmpeg_eq_contrast_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: EqFilter.IsValidParameter(contrast=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_CONTRAST_MAX,
            "name": "ffmpeg_eq_contrast_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (EqFilter.IsValidParameter(contrast=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_EQ_CONTRAST_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_BRIGHTNESS_MIN,
            "name": "ffmpeg_eq_brightness_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: EqFilter.IsValidParameter(brightness=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_BRIGHTNESS_MAX,
            "name": "ffmpeg_eq_brightness_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (EqFilter.IsValidParameter(brightness=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_EQ_BRIGHTNESS_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_SATURATION_MIN,
            "name": "ffmpeg_eq_saturation_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: EqFilter.IsValidParameter(saturation=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_SATURATION_MAX,
            "name": "ffmpeg_eq_saturation_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (EqFilter.IsValidParameter(saturation=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_EQ_SATURATION_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_GAMMA_MIN,
            "name": "ffmpeg_eq_gamma_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: EqFilter.IsValidParameter(gamma=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_EQ_GAMMA_MAX,
            "name": "ffmpeg_eq_gamma_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (EqFilter.IsValidParameter(gamma=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_EQ_GAMMA_MIN)),
        },
        # fps
        {
            "type": FfmpegConfigTypes.FFMPEG_FPS_ENABLED,
            "name": "ffmpeg_fps_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_FPS_MIN,
            "name": "ffmpeg_fps_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: FpsFilter.IsValidParameter(val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_FPS_MAX,
            "name": "ffmpeg_fps_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (FpsFilter.IsValidParameter(val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_FPS_MIN)),
        },
        # hflip
        {
            "type": FfmpegConfigTypes.FFMPEG_HFLIP_ENABLED,
            "name": "ffmpeg_hflip_enabled",
            "conv_fct": Utils.StrToBool,
        },
        # noise
        {
            "type": FfmpegConfigTypes.FFMPEG_NOISE_ENABLED,
            "name": "ffmpeg_noise_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_NOISE_ALLF,
            "name": "ffmpeg_noise_allf",
            "valid_if": lambda cfg, val: NoiseFilter.IsValidParameter(allf=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_NOISE_ALLS_MIN,
            "name": "ffmpeg_noise_alls_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: NoiseFilter.IsValidParameter(alls=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_NOISE_ALLS_MAX,
            "name": "ffmpeg_noise_alls_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (NoiseFilter.IsValidParameter(alls=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_NOISE_ALLS_MIN)),
        },
        # output format
        {
            "type": FfmpegConfigTypes.FFMPEG_OUTPUT_FORMAT,
            "name": "ffmpeg_output_format",
            "valid_if": lambda cfg, val: OutputFormatFilter.IsValidParameter(val),
        },
        # scale
        {
            "type": FfmpegConfigTypes.FFMPEG_SCALE_ENABLED,
            "name": "ffmpeg_scale_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SCALE_ALGO,
            "name": "ffmpeg_scale_algo",
            "valid_if": lambda cfg, val: ScaleFilter.IsValidParameter(flags=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SCALE_H,
            "name": "ffmpeg_scale_h",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: ScaleFilter.IsValidParameter(h=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SCALE_W,
            "name": "ffmpeg_scale_w",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: ScaleFilter.IsValidParameter(w=val),
        },
        # smartblur
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_ENABLED,
            "name": "ffmpeg_smartblur_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_LR_MIN,
            "name": "ffmpeg_smartblur_lr_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: SmartblurFilter.IsValidParameter(lr=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_LR_MAX,
            "name": "ffmpeg_smartblur_lr_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (SmartblurFilter.IsValidParameter(lr=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_SMARTBLUR_LR_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_LS_MIN,
            "name": "ffmpeg_smartblur_ls_min",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: SmartblurFilter.IsValidParameter(ls=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_LS_MAX,
            "name": "ffmpeg_smartblur_ls_max",
            "conv_fct": Utils.StrToFloat,
            "valid_if": lambda cfg, val: (SmartblurFilter.IsValidParameter(ls=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_SMARTBLUR_LS_MIN)),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_LT_MIN,
            "name": "ffmpeg_smartblur_lt_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: SmartblurFilter.IsValidParameter(lt=val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_SMARTBLUR_LT_MAX,
            "name": "ffmpeg_smartblur_lt_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (SmartblurFilter.IsValidParameter(lt=val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_SMARTBLUR_LT_MIN)),
        },
        # vbitrate
        {
            "type": FfmpegConfigTypes.FFMPEG_VBITRATE_ENABLED,
            "name": "ffmpeg_vbitrate_enabled",
            "conv_fct": Utils.StrToBool,
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_VBITRATE_MIN,
            "name": "ffmpeg_vbitrate_min",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: VBitrateFilter.IsValidParameter(val),
        },
        {
            "type": FfmpegConfigTypes.FFMPEG_VBITRATE_MAX,
            "name": "ffmpeg_vbitrate_max",
            "conv_fct": Utils.StrToInt,
            "valid_if": lambda cfg, val: (VBitrateFilter.IsValidParameter(val) and
                                          val >= cfg.GetValue(FfmpegConfigTypes.FFMPEG_VBITRATE_MIN)),
        },
    ],
}
