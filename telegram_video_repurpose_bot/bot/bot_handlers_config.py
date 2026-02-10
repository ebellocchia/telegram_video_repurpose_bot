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

from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler, MessageHandler

from telegram_video_repurpose_bot.bot.bot_handlers_config_typing import BotHandlersConfigType
from telegram_video_repurpose_bot.command.command_dispatcher import CommandTypes
from telegram_video_repurpose_bot.message.message_dispatcher import MessageTypes


BotHandlersConfig: BotHandlersConfigType = {
    MessageHandler: [
        {
            "callback": lambda self, client, message: self.DispatchCommand(client,
                                                                           message,
                                                                           CommandTypes.ALIVE_CMD),
            "filters": filters.private & filters.command(["alive"]),
        },
        {
            "callback": lambda self, client, message: self.DispatchCommand(client,
                                                                           message,
                                                                           CommandTypes.HELP_CMD,
                                                                           user_menu=self.user_menu),
            "filters": filters.private & filters.command(["help", "start"]),
        },
        {
            "callback": (lambda self, client, message: self.HandleMessage(client,
                                                                          message,
                                                                          MessageTypes.GROUP_CHAT_CREATED)),
            "filters": filters.group_chat_created,
        },
        {
            "callback": (lambda self, client, message: self.HandleMessage(client,
                                                                          message,
                                                                          MessageTypes.NEW_CHAT_MEMBERS)),
            "filters": filters.new_chat_members,
        },
        {
            "callback": (lambda self, client, message: self.HandleMessage(client,
                                                                          message,
                                                                          MessageTypes.LEFT_CHAT_MEMBER)),
            "filters": filters.left_chat_member,
        },
        {
            "callback": (lambda self, client, message: self.HandleMessage(client,
                                                                          message,
                                                                          MessageTypes.PRIVATE,
                                                                          user_menu=self.user_menu)),
            "filters": filters.private,
        },
    ],
    CallbackQueryHandler: [
        {
            "callback": lambda self, client, cbk_query: self.DispatchCallbackQuery(client,
                                                                                   cbk_query,
                                                                                   user_menu=self.user_menu),
            "filters": None,
        },
    ],
}
