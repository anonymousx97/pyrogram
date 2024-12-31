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

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types, utils, enums
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType
from ..object import Object


class ExternalReplyInfo(Object):
    """This object contains information about a message that is being replied to, which may come from another chat or forum topic.

    Parameters:
        origin (:obj:`~pyrogram.types.User`, *optional*):
            Origin of the message replied to by the given message

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Chat the original message belongs to. Available only if the chat is a supergroup or a channel.

        message_id  (``int``, *optional*):
            Unique message identifier inside the original chat. Available only if the original chat is a supergroup or a channel.

        link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
            Options used for link preview generation for the original message, if it is a text message

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Message is an animation, information about the animation.

        audio (:obj:`~pyrogram.types.Audio`, *optional*):
            Message is an audio file, information about the file.

        document (:obj:`~pyrogram.types.Document`, *optional*):
            Message is a general file, information about the file.

        paid_media (:obj:`~pyrogram.types.PaidMediaInfo`, *optional*):
            Message contains paid media; information about the paid media.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Message is a photo, information about the photo.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Message is a sticker, information about the sticker.

        story (:obj:`~pyrogram.types.Story`, *optional*):
            Message is a forwarded story.

        video (:obj:`~pyrogram.types.Video`, *optional*):
            Message is a video, information about the video.

        video_note (:obj:`~pyrogram.types.VideoNote`, *optional*):
            Message is a video note, information about the video message.

        voice (:obj:`~pyrogram.types.Voice`, *optional*):
            Message is a voice message, information about the file.

        has_media_spoiler (``bool``, *optional*):
            True, if the message media is covered by a spoiler animation.

        contact (:obj:`~pyrogram.types.Contact`, *optional*):
            Message is a shared contact, information about the contact.

        dice (:obj:`~pyrogram.types.Dice`, *optional*):
            A dice containing a value that is randomly generated by Telegram.

        game (:obj:`~pyrogram.types.Game`, *optional*):
            Message is a game, information about the game.
        
        giveaway (:obj:`~pyrogram.types.Giveaway`, *optional*):
            Message is a scheduled giveaway, information about the giveaway

        giveaway_winners (:obj:`~pyrogram.types.GiveawayWinners`, *optional*):
            A giveaway with public winners was completed

        invoice (:obj:`~pyrogram.types.Invoice`, *optional*):
            Message is an invoice for a `payment <https://core.telegram.org/bots/api#payments>`_, information about the invoice. `More about payments » <https://core.telegram.org/bots/api#payments>`_

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Message is a shared location, information about the location.

        poll (:obj:`~pyrogram.types.Poll`, *optional*):
            Message is a native poll, information about the poll.

        venue (:obj:`~pyrogram.types.Venue`, *optional*):
            Message is a venue, information about the venue.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        origin: "types.MessageOrigin" = None,
        chat: "types.Chat" = None,
        message_id: int,
        link_preview_options: "types.LinkPreviewOptions" = None,
        animation: "types.Animation" = None,
        audio: "types.Audio" = None,
        document: "types.Document" = None,
        paid_media: "types.PaidMediaInfo" = None,
        photo: "types.Photo" = None,
        sticker: "types.Sticker" = None,
        story: "types.Story" = None,
        video: "types.Video" = None,
        video_note: "types.VideoNote" = None,
        voice: "types.Voice" = None,
        has_media_spoiler: bool = None,
        contact: "types.Contact" = None,
        dice: "types.Dice" = None,
        game: "types.Game" = None,
        giveaway: "types.Giveaway" = None,
        giveaway_winners: "types.GiveawayWinners" = None,
        invoice: "types.Invoice" = None,
        location: "types.Location" = None,
        poll: "types.Poll" = None,
        venue: "types.Venue" = None,
    ):
        super().__init__(client)

        self.origin = origin
        self.chat = chat
        self.message_id = message_id
        self.link_preview_options = link_preview_options
        self.animation = animation
        self.audio = audio
        self.document = document
        self.paid_media = paid_media
        self.photo = photo
        self.sticker = sticker
        self.story = story
        self.video = video
        self.video_note = video_note
        self.voice = voice
        self.has_media_spoiler = has_media_spoiler
        self.contact = contact
        self.dice = dice
        self.game = game
        self.giveaway = giveaway
        self.giveaway_winners = giveaway_winners
        self.invoice = invoice
        self.location = location
        self.poll = poll
        self.venue = venue

    @staticmethod
    async def _parse(
        client,
        chats: dict,
        users: dict,
        reply_to: "raw.types.MessageReplyHeader"
    ) -> "ExternalReplyInfo":
        if not getattr(reply_to, "reply_from", None):
            # TODO: temp. workaround
            return None

        if isinstance(reply_to, raw.types.MessageReplyHeader):
            reply_from = reply_to.reply_from  # raw.types.MessageFwdHeader
            origin = types.MessageOrigin._parse(
                client,
                reply_from,
                users,
                chats,
            )

            chat = None
            if isinstance(reply_to.reply_to_peer_id, raw.types.PeerChannel):
                raw_peer_id = utils.get_raw_peer_id(reply_to.reply_to_peer_id)
                chat = types.Chat._parse_chat(
                    client,
                    chats[raw_peer_id],
                )

            animation = None
            audio = None
            document = None
            paid_media = None
            photo = None
            sticker = None
            story = None
            video = None
            video_note = None
            voice = None

            has_media_spoiler = None

            contact = None
            dice = None
            game = None
            giveaway = None
            giveaway_winners = None
            invoice = None
            location = None
            poll = None
            venue = None
            
            web_page = None
            link_preview_options = types.LinkPreviewOptions._parse(
                client,
                reply_to.reply_media,
                None,
                False
            )

            media = reply_to.reply_media
            media_type = None
            
            if media:
                if isinstance(media, raw.types.MessageMediaPhoto):
                    photo = types.Photo._parse(
                        client,
                        media.photo,
                        media.ttl_seconds,
                        media.spoiler
                    )
                    media_type = enums.MessageMediaType.PHOTO
                    has_media_spoiler = media.spoiler
                elif isinstance(media, raw.types.MessageMediaGeo):
                    location = types.Location._parse(client, media.geo)
                    media_type = enums.MessageMediaType.LOCATION
                elif isinstance(media, raw.types.MessageMediaContact):
                    contact = types.Contact._parse(client, media)
                    media_type = enums.MessageMediaType.CONTACT
                elif isinstance(media, raw.types.MessageMediaVenue):
                    venue = types.Venue._parse(client, media)
                    media_type = enums.MessageMediaType.VENUE
                elif isinstance(media, raw.types.MessageMediaGame):
                    game = types.Game._parse(client, media.game)
                    media_type = enums.MessageMediaType.GAME
                elif isinstance(media, raw.types.MessageMediaDocument):
                    doc = media.document

                    if isinstance(doc, raw.types.Document):
                        attributes = {type(i): i for i in doc.attributes}

                        file_name = getattr(
                            attributes.get(
                                raw.types.DocumentAttributeFilename, None
                            ), "file_name", None
                        )

                        if raw.types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                            animation = types.Animation._parse(client, doc, video_attributes, file_name)
                            media_type = enums.MessageMediaType.ANIMATION
                            has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeSticker in attributes:
                            sticker = await types.Sticker._parse(client, doc, attributes)
                            media_type = enums.MessageMediaType.STICKER
                        elif raw.types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[raw.types.DocumentAttributeVideo]

                            if video_attributes.round_message:
                                video_note = types.VideoNote._parse(client, doc, video_attributes)
                                media_type = enums.MessageMediaType.VIDEO_NOTE
                            else:
                                video = types.Video._parse(client, doc, video_attributes, file_name, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VIDEO
                                has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[raw.types.DocumentAttributeAudio]

                            if audio_attributes.voice:
                                voice = types.Voice._parse(client, doc, audio_attributes)
                                media_type = enums.MessageMediaType.VOICE
                            else:
                                audio = types.Audio._parse(client, doc, audio_attributes, file_name)
                                media_type = enums.MessageMediaType.AUDIO
                        else:
                            document = types.Document._parse(client, doc, file_name)
                            media_type = enums.MessageMediaType.DOCUMENT
                elif isinstance(media, raw.types.MessageMediaWebPage):
                    if isinstance(media.webpage, raw.types.WebPage):
                        web_page = types.WebPage._parse(client, media.webpage)
                        media_type = enums.MessageMediaType.WEB_PAGE
                        web_page_url = media.webpage.url
                    else:
                        media = None
                elif isinstance(media, raw.types.MessageMediaPoll):
                    poll = types.Poll._parse(client, media)
                    media_type = enums.MessageMediaType.POLL
                elif isinstance(media, raw.types.MessageMediaDice):
                    dice = types.Dice._parse(client, media)
                    media_type = enums.MessageMediaType.DICE
                elif isinstance(media, raw.types.MessageMediaStory):
                    story = await types.Story._parse(client, users, chats, media, None, None, None, None)
                    media_type = enums.MessageMediaType.STORY
                elif isinstance(media, raw.types.MessageMediaGiveaway):
                    giveaway = types.Giveaway._parse(client, chats, media)
                    media_type = enums.MessageMediaType.GIVEAWAY
                elif isinstance(media, raw.types.MessageMediaGiveawayResults):
                    giveaway_winners = types.GiveawayWinners._parse(client, chats, users, media)
                    media_type = enums.MessageMediaType.GIVEAWAY_WINNERS
                elif isinstance(media, raw.types.MessageMediaInvoice):
                    invoice = types.Invoice._parse(client, media)
                    media_type = enums.MessageMediaType.INVOICE
                elif isinstance(media, raw.types.MessageMediaPaidMedia):
                    paid_media = types.PaidMediaInfo._parse(client, media)
                    media_type = enums.MessageMediaType.PAID_MEDIA

            return ExternalReplyInfo(
                origin=origin,
                chat=chat,
                message_id=reply_to.reply_to_msg_id,
                link_preview_options=link_preview_options,
                animation=animation,
                audio=audio,
                document=document,
                paid_media=paid_media,
                photo=photo,
                sticker=sticker,
                story=story,
                video=video,
                video_note=video_note,
                voice=voice,
                has_media_spoiler=has_media_spoiler,
                contact=contact,
                dice=dice,
                game=game,
                giveaway=giveaway,
                giveaway_winners=giveaway_winners,
                invoice=invoice,
                location=location,
                poll=poll,
                venue=venue
            )
