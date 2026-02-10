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

from enum import Enum
from typing import Any, Dict, List, Optional

import pyrogram

from telegram_video_repurpose_bot.utils.wrapped_dict import WrappedDict


class MenuStateParam(WrappedDict):
    """
    Stores parameters for a single menu state with formatted string representation.

    Wraps dictionary operations for state-specific parameters, providing
    methods to convert parameters to readable string format for logging.
    """

    def ToString(self) -> str:
        """
        Convert parameters to string representation.

        Returns:
            String representation of the parameters, or 'Empty' if no parameters exist.
        """
        if self.Count() == 0:
            return "Empty"

        msg = ""
        for key, value in self.dict_elements.items():
            key_str = key.name.lower() if isinstance(key, Enum) else str(key)
            if hasattr(value, "Id"):
                msg += f"{key_str} ID: {value.Id()}, "
            elif isinstance(value, Enum):
                msg += f"{key_str}: {value.name.lower()}, "
            else:
                msg += f"{key_str}: {value}, "
        return msg.rstrip(", ")

    def __str__(self) -> str:
        """
        Convert to string.

        Returns:
            String representation of the parameters.
        """
        return self.ToString()


class MenuStateParams:
    """
    Manages state parameters for multiple users.

    Maintains per-user state parameters with methods to add, retrieve, and
    clear parameters while optionally preserving specific keys during cleanup.
    """

    user_params: Dict[int, MenuStateParam]

    def __init__(self) -> None:
        """Initialize menu state parameters storage."""
        self.user_params = {}

    def ClearByUser(self,
                    user: pyrogram.types.User,
                    except_keys: Optional[List[Any]] = None) -> None:
        """
        Clear parameters for a specific user, optionally preserving certain keys.

        Args:
            user: The user whose parameters should be cleared.
            except_keys: Optional list of keys to preserve during clearing.
        """
        if not self.ExistsByUser(user):
            return
        except_keys = except_keys or []
        saved_keys = {
            key: self.user_params[user.id][key] for key in except_keys if key in self.user_params[user.id]
        }
        self.user_params[user.id].Clear()
        self.user_params[user.id].AddMultiple(saved_keys)

    def ExistsByUser(self,
                     user: pyrogram.types.User) -> bool:
        """
        Check if parameters exist for a specific user.

        Args:
            user: The user to check.

        Returns:
            True if parameters exist for the user, False otherwise.
        """
        return user.id in self.user_params

    def GetByUser(self,
                  user: pyrogram.types.User) -> MenuStateParam:
        """
        Get parameters for a specific user, creating them if necessary.

        Args:
            user: The user to get parameters for.

        Returns:
            The MenuStateParam object for the user.
        """
        if not self.ExistsByUser(user):
            self.user_params[user.id] = MenuStateParam()
        return self.user_params[user.id]
