import discord
from redbot.core import commands, app_commands, Config
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import asyncio
import functools
import regex as re
from .functions_js import (
    COLOR_CHOICES,
    CHARACTER_CHOICES,
    CHOICES,
    CHOICE_DESC,
    generate,
    convert_to_discord_file,
)
import logging

from typing import Optional, Union, Tuple, Coroutine, Any


class Umineko(commands.Cog):
    """Umineko Screenshot Generator"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__version__ = "1.0.0"
        self.message = None
        self.embed = discord.Embed(title="Umineko", description="a.")
        self.color = None
        self.log = logging.getLogger("glas.glas-cogs.umineko")

    async def generate_image(self, task: commands.Context):
        task = self.bot.loop.run_in_executor(None, task)
        try:
            image = await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            return "An error occurred while generating this sticker. Try again later."
        else:
            return image

    @app_commands.command(name="umi", description="Umineko Background Generator")
    @app_commands.describe(**CHOICE_DESC)
    @app_commands.choices(
        **CHOICES,
    )
    async def umi_command(
        self,
        ctx: commands.Context,
        text1: str,
        text2: Optional[str],
        left: Optional[str],
        center: Optional[str],
        right: Optional[str],
        metaleft: Optional[str],
        metacenter: Optional[str],
        metaright: Optional[str],
        color1: Optional[str],
        color2: Optional[str],
        bg: Optional[str],
    ):
        """Make a Umineko Screenshot!"""
        parameters = {
            "text1": text1,
            "text2": text2,
            "left": left,
            "center": center,
            "right": right,
            "metaleft": metaleft,
            "metacenter": metacenter,
            "metaright": metaright,
            "color1": color1,
            "color2": color2,
            "bg": bg,
        }

        try:
            image = await self.generate_image(ctx, **parameters)
            await ctx.send(file=image) if isinstance(
                image, discord.File
            ) else await ctx.send(image)
        except Exception as e:
            # Handle the exception, e.g., log it or inform the user
            await ctx.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )


async def generate_image(ctx, **kwargs):
    """Generate Umineko Screenshot and return the image."""
    # Core logic for Umineko screenshot generation using kwargs and ctx

    # Replace the following line with your actual image generation logic
    image_data = generate(**kwargs)

    # For simplicity, assume there's a method to convert image_data to a Discord File
    image_file = convert_to_discord_file(image_data)

    return image_file
