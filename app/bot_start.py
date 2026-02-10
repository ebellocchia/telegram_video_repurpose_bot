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

import argparse
import asyncio

from telegram_video_repurpose_bot import VideoRepurposeBot, __version__


DEF_CONFIG_FILE = "conf/config.ini"


class ArgumentsParser:
    """Parses command-line arguments for bot startup.

    Handles configuration file path specification with a default
    configuration file location if not explicitly provided.
    """

    parser: argparse.ArgumentParser

    def __init__(self) -> None:
        """Initialize the argument parser."""
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "-c", "--config",
            type=str,
            default=DEF_CONFIG_FILE,
            help="configuration file"
        )

    def Parse(self) -> argparse.Namespace:
        """Parse command line arguments.

        Returns:
            Parsed arguments as an argparse.Namespace object.
        """
        return self.parser.parse_args()


def print_header() -> None:
    """Print the application header with version information."""
    print("")
    print("**************************************")
    print("****                              ****")
    print("***                                ***")
    print("**                                  **")
    print("*    Telegram Video Repurpose Bot    *")
    print("*     Author: Emanuele Bellocchia    *")
    print(f"*           Version: {__version__}           *")
    print("**                                  **")
    print("***                                ***")
    print("****                              ****")
    print("**************************************")
    print("")


async def main() -> None:
    """Main async entry point for the bot."""
    print_header()
    args_parser = ArgumentsParser()
    args = args_parser.Parse()
    bot = VideoRepurposeBot(args.config)
    await bot.Run()


if __name__ == "__main__":
    asyncio.run(main())
