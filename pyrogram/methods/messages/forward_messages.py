#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw, utils
from pyrogram import types


class ForwardMessages:
    async def forward_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        message_thread_id: int = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        drop_author: bool = None,
        drop_media_captions: bool = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None
    ) -> Union["types.Message", List["types.Message"]]:
        """Forward messages of any kind.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original message was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``):
                An iterable of message identifiers in the chat specified in *from_chat_id* or a single message id.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum; for forum supergroups only

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            drop_author (``bool``, *optional*):
                Whether to forward messages without quoting the original author.

            drop_media_captions (``bool``, *optional*):
                Whether to strip captions from media.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.
        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Forward a single message
                await app.forward_messages(to_chat, from_chat, 123)

                # Forward multiple messages at once
                await app.forward_messages(to_chat, from_chat, [1, 2, 3])
        """

        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]

        r = await self.invoke(
            raw.functions.messages.ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),
                from_peer=await self.resolve_peer(from_chat_id),
                id=message_ids,
                silent=disable_notification or None,
                # TODO
                # TODO
                drop_author=drop_author,
                drop_media_captions=drop_media_captions,
                noforwards=protect_content,
                random_id=[self.rnd_id() for _ in message_ids],
                send_as=await self.resolve_peer(send_as) if send_as else None,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                top_msg_id=message_thread_id
                # TODO
            )
        )

        forwarded_messages = []

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage
                )
            ):
                forwarded_messages.append(
                    await types.Message._parse(
                        self,
                        i.message,
                        users,
                        chats,
                        is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                        replies=self.fetch_replies
                    )
                )

        return types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
