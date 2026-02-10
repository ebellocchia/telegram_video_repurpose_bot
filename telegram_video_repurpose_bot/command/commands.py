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

from typing import Any

from typing_extensions import override

from telegram_video_repurpose_bot.command.command_base import CommandBase


class HelpCmd(CommandBase):
    """Command for getting help."""

    @override
    async def _ExecuteCommand(self,
                              **kwargs: Any) -> None:
        """
        Execute command implementation.

        Args:
            **kwargs: Additional keyword arguments including:
                - user_menu: User menu instance for resetting the menu state.
        """
        await kwargs["user_menu"].Reset(self.cmd_data.Chat(), self.cmd_data.User())


class AliveCmd(CommandBase):
    """Command for checking is the bot is alive."""

    @override
    async def _ExecuteCommand(self,
                              **kwargs: Any) -> None:
        """
        Execute command implementation.

        Args:
            **kwargs: Additional keyword arguments including:
                - user_menu: User menu instance for resetting the menu state.
        """
        await self._SendMessage(self.translator.GetSentence("ALIVE_MSG"))
