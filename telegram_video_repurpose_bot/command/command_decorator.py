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

from typing import Any, Callable, Coroutine

from telegram_video_repurpose_bot.app.app_users import AppUsers
from telegram_video_repurpose_bot.misc.helpers import UserHelper


def AdminUsersOnly(exec_cmd_fct: Callable[..., Coroutine[Any, Any, None]]) -> Callable[..., Coroutine[Any, Any, None]]:
    """
    Decorator for admin users only commands.

    Args:
        exec_cmd_fct: Command execution function

    Returns:
        Callable[..., Coroutine[Any, Any, None]]: Decorated async function
    """
    async def decorated(self,
                        **kwargs: Any) -> None:
        if not AppUsers(self.bot_config).IsAdmin(self.cmd_data.User()):
            if self._IsPrivateChat():
                await self._SendMessage(self.translator.GetSentence("CMD_USER_AUTH_ERR_MSG"))
                self.logger.GetLogger().warning(
                    f"User {UserHelper.GetNameOrId(self.cmd_data.User())} tried to execute the command "
                    f"but it's not authorized"
                )
        else:
            await exec_cmd_fct(self, **kwargs)

    return decorated


def AuthorizedUsersOnly(exec_cmd_fct: Callable[..., Coroutine[Any, Any, None]]) -> Callable[..., Coroutine[Any, Any, None]]:
    """
    Decorator for authorized users only commands.

    Args:
        exec_cmd_fct: Command execution function

    Returns:
        Callable[..., Coroutine[Any, Any, None]]: Decorated async function
    """
    async def decorated(self,
                        **kwargs: Any) -> None:
        if not AppUsers(self.bot_config).IsAuthorized(self.cmd_data.User()):
            if self._IsPrivateChat():
                await self._SendMessage(self.translator.GetSentence("CMD_USER_AUTH_ERR_MSG"))
                self.logger.GetLogger().warning(
                    f"User {UserHelper.GetNameOrId(self.cmd_data.User())} tried to execute the command "
                    f"but it's not authorized"
                )
        else:
            await exec_cmd_fct(self, **kwargs)

    return decorated
