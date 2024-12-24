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

import pyrogram
from pyrogram import raw


class UpdateProfile:
    async def update_profile(
        self: "pyrogram.Client",
        *,
        first_name: str = None,
        last_name: str = None,
        bio: str = None
    ) -> bool:
        """Update your profile details such as first name, last name and bio.

        You can omit the parameters you don't want to change.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            first_name (``str``, *optional*):
                The new first name; 1-64 characters.

            last_name (``str``, *optional*):
                The new last name; 1-64 characters.
                Pass "" (empty string) to remove it.

            bio (``str``, *optional*):
                Changes the bio of the current user.
                Max ``intro_description_length_limit`` characters without line feeds.
                Pass "" (empty string) to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your first name only
                await app.update_profile(first_name="Pyrogram")

                # Update first name and bio
                await app.update_profile(first_name="Pyrogram", bio="https://docs.pyrogram.org/")

                # Remove the last name
                await app.update_profile(last_name="")
        """

        if first_name:
            self.app_constant.check_valid_length(
                text=first_name,
                arg_type="first_name",
                max_length_tye="MAX_USER_FIRSTNAME_LENGTH"
            )

        if last_name:
            self.app_constant.check_valid_length(
                text=last_name,
                arg_type="last_name",
                max_length_tye="MAX_USER_LASTNAME_LENGTH"
            )

        if bio:
            self.app_constant.check_valid_length(
                text=bio,
                arg_type="bio",
                max_length_tye=(
                    "MAX_PREMIUM_USERBIO_LENGTH"
                    if self.me and self.me.is_premium
                    else "MAX_USERBIO_LENGTH"
                )
            )

        return bool(
            await self.invoke(
                raw.functions.account.UpdateProfile(
                    first_name=first_name,
                    last_name=last_name,
                    about=bio
                )
            )
        )
